from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
PACKAGE=Path(__file__).resolve().parents[1]; SKILLS=PACKAGE.parents[1]; LOCAL=PACKAGE/'runtime'
for path in (SKILLS,LOCAL):
    if str(path) not in sys.path: sys.path.insert(0,str(path))
import execute, invoke, record
from runtime.io import CommandError

class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name)/'repo'; self.inputs=Path(self.tmp.name)/'inputs'; self.inputs.mkdir(); subprocess.run(['git','init','-q','-b','main',str(self.repo)],check=True); self.git('config','user.name','Test'); self.git('config','user.email','test@example.invalid'); (self.repo/'base.txt').write_text('old\n'); self.git('add','.'); self.git('commit','-qm','old base'); self.old=self.git('rev-parse','HEAD'); (self.repo/'base.txt').write_text('new\n'); self.git('commit','-qam','new base'); self.new=self.git('rev-parse','HEAD'); self.git('switch','-qc','feature',self.old); (self.repo/'task.txt').write_text('task\n'); self.git('add','.'); self.git('commit','-qm','task'); self.head=self.git('rev-parse','HEAD'); self.task_ref='.trellis/tasks/current'; self.task_dir=self.repo/self.task_ref; self.task_dir.mkdir(parents=True); self.task_id='current-task'; self.write_identity()
    def tearDown(self): self.tmp.cleanup()
    def git(self,*args): return subprocess.run(['git',*args],cwd=self.repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()
    def write(self,name,value): path=self.inputs/name; path.write_text(json.dumps(value)); return path
    def write_identity(self,status='in_progress',branch='feature',task_ref=None,task_id=None,workspace_path=None):
        task_ref=task_ref or self.task_ref; task_id=task_id or self.task_id; workspace_path=workspace_path or str(self.repo.resolve()); task_dir=self.repo/task_ref; task_dir.mkdir(parents=True,exist_ok=True); (task_dir/'task.json').write_text(json.dumps({'id':task_id,'status':status,'branch':branch,'base_branch':'main'}))
        tasks=self.repo/'.trellis/.runtime/guru-team/tasks'; workspaces=self.repo/'.trellis/.runtime/guru-team/workspaces'; tasks.mkdir(parents=True,exist_ok=True); workspaces.mkdir(parents=True,exist_ok=True)
        (tasks/f'{task_id}.json').write_text(json.dumps({'schema_version':'1.0','task_slug':task_id,'workspace_slug':task_id,'workspace_path':workspace_path,'task_artifact_dir':task_ref}))
        (workspaces/f'{task_id}.json').write_text(json.dumps({'schema_version':'1.0','workspace_slug':task_id,'workspace_path':workspace_path,'branch_name':branch}))
    def runtime_snapshot(self):
        root=self.repo/'.trellis/.runtime'; return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
    def public(self, profile='post_check'):
        targets={'post_plan':'task_activation','post_check':'task_commit','post_commit':'branch_review','post_branch_review':'publication_review','post_publication':'task_finalization','finalizer_base_mismatch':'finalization_resume'}
        value={'profile':profile,'mode':'workflow','task_ref':self.task_ref,'task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'resume_target':targets[profile]}
        if profile in {'post_branch_review','post_publication','finalizer_base_mismatch'}: value['branch_review_commit']=self.head
        return value
    def gate(self): return {'authority_impact':'unchanged','task_content_impact':'unchanged','integration_impact':'compatible','reviewed_scope':['authority','planning','delta'],'key_delta_refs':['base.txt'],'validation_evidence':['candidate clean'],'unverified_boundaries':[],'summary':'Compatible.','typed_exit':'reconciled','route_payload':{}}
    def test_guard_unchanged_and_new_pair_write_nothing(self):
        before=self.runtime_snapshot(); public=self.public(); path=self.write('public.json',public); self.assertEqual('new_pair',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status']); public['old_base_head']=self.new; path=self.write('same.json',public); self.assertEqual('unchanged',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status']); self.assertEqual(before,self.runtime_snapshot())
    def test_all_boundaries_unchanged_are_zero_write_and_need_no_review_identity(self):
        for profile in ('post_plan','post_check','post_commit','post_branch_review','post_publication','finalizer_base_mismatch'):
            public=self.public(profile); public['old_base_head']=self.new
            result=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write(profile+'.json',public))])
            self.assertEqual('unchanged',result['status'],profile)
        self.assertNotIn('branch_review_commit',self.public('post_commit'))
    def test_multiple_base_commits_form_one_cumulative_pair(self):
        self.git('switch','main'); (self.repo/'second.txt').write_text('second\n'); self.git('add','second.txt'); self.git('commit','-qm','second base advance'); newest=self.git('rev-parse','HEAD'); self.git('switch','feature')
        public=self.public(); public['selected_base_ref']=newest; public['new_base_head']=newest
        result=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write('cumulative.json',public))])
        self.assertEqual('new_pair',result['status']); self.assertEqual(self.old,result['old_base_head']); self.assertEqual(newest,result['new_base_head'])
    def test_candidate_is_clean_and_leaves_no_worktree(self):
        request=self.write('request.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[['git','status','--short']]}); result=execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)]); self.assertEqual('clean',result['merge_status']); self.assertRegex(result['candidate_tree_sha256'],r'^[0-9a-f]{64}$'); self.assertEqual([],result['conflict_paths']); self.assertNotIn('guru-base-candidate-',self.git('worktree','list'))
    def test_record_invoke_consumes_checkpoint_once(self):
        public=self.public(); pi=self.write('public.json',public); gate=self.write('gate.json',self.gate()); result=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gate),'--typed-exit','reconciled']); envelope=self.write('envelope.json',{'public_input':public,'owner_result':result}); output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)]); self.assertEqual('reconciled',output['exit_id']); checkpoint=self.repo/'.trellis/.runtime/guru-team/owner-checkpoints/current/guru-reconcile-task-base/base-reconciliation.json'; self.assertFalse(checkpoint.exists())
        with self.assertRaises(CommandError) as raised:
            invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])
        self.assertEqual('stale_identity',raised.exception.code)
    def test_reconciled_requires_complete_compatible_evidence(self):
        public=self.public(); pi=self.write('reconciled-public.json',public)
        mutations=(('authority_impact','insufficient_evidence'),('task_content_impact','insufficient_evidence'),('integration_impact','insufficient_evidence'),('unverified_boundaries',['live validation unavailable']))
        for field,value in mutations:
            with self.subTest(field=field):
                gate=self.gate(); gate[field]=value; gate_path=self.write('invalid-'+field+'.json',gate)
                with self.assertRaises(CommandError) as raised:
                    record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled'])
                self.assertEqual('schema_mismatch',raised.exception.code)
    def test_current_pair_preserves_each_semantic_exit_and_retires_once(self):
        cases={
            'reconciled':('post_check',{}),
            'review_continuity_required':('post_branch_review',{'candidate_tree_sha256':'d'*64,'relevant_paths':['base.txt']}),
            'implementation_required':('post_check',{'finding_refs':['finding-1']}),
            'planning_stale':('post_check',{'reason_refs':['planning-1']}),
            'scope_confirmation_required':('post_check',{'proposal_refs':['proposal-1']}),
            'blocked':('post_check',{}),
        }
        for exit_id,(profile,payload) in cases.items():
            with self.subTest(exit_id=exit_id):
                public=self.public(profile); pi=self.write(exit_id+'-public.json',public); gate=self.gate(); gate.update({'typed_exit':exit_id,'route_payload':payload}); gp=self.write(exit_id+'-gate.json',gate)
                owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gp),'--typed-exit',exit_id])
                guarded=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(pi)])
                self.assertEqual('current_pair',guarded['status']); self.assertEqual(owner['typed_output'],guarded['typed_output'])
                self.assertEqual('new_pair',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(pi)])['status'])
    def test_132_161_replay_preserves_review_head_and_resumes_finalizer(self):
        public=self.public('finalizer_base_mismatch'); pi=self.write('historical-finalizer.json',public); gate=self.gate(); gate['reviewed_scope'].append('historical #132/#161 base-only stale route'); gp=self.write('historical-gate.json',gate)
        result=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gp),'--typed-exit','reconciled']); envelope=self.write('historical-envelope.json',{'public_input':public,'owner_result':result}); output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])
        self.assertEqual('finalization_resume',output['resume_target']); self.assertEqual(self.head,public['branch_review_commit']); self.assertNotIn('branch_review_commit',output)
    def test_history_rewrite_blocks(self):
        public=self.public(); public['old_base_head']=self.head; path=self.write('bad.json',public); self.assertEqual('blocked',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status'])
    def test_task_identity_rejects_typo_status_branch_mapping_and_not_current(self):
        cases=[]
        typo=self.public(); typo['task_ref']='.trellis/tasks/typo'; cases.append(('typo',typo,lambda:None))
        stale=self.public(); cases.append(('status',stale,lambda:self.write_identity(status='done')))
        wrong_branch=self.public(); cases.append(('branch',wrong_branch,lambda:self.write_identity(branch='other')))
        stale_mapping=self.public(); cases.append(('mapping',stale_mapping,lambda:self.write_identity(workspace_path=str(self.repo.parent/'other'))))
        other_ref='.trellis/tasks/other'; self.write_identity(task_ref=other_ref,task_id='other-task'); not_current=self.public(); not_current['task_ref']=other_ref; cases.append(('not-current',not_current,lambda:None))
        for name,public,mutate in cases:
            with self.subTest(name=name):
                self.write_identity(); mutate(); path=self.write('identity-'+name+'.json',public)
                with self.assertRaises(CommandError) as raised:
                    execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])
                self.assertEqual('stale_identity',raised.exception.code)
    def test_checkpoint_namespace_binds_task_id_and_full_ref(self):
        from common import checkpoint_path
        first=checkpoint_path(self.repo,self.task_ref)
        (self.repo/'.trellis/.runtime/guru-team/tasks'/f'{self.task_id}.json').unlink()
        nested='.trellis/tasks/nested/current'; self.write_identity(task_ref=nested,task_id='nested-current')
        second=checkpoint_path(self.repo,nested)
        self.assertNotEqual(first.parent.parent.name,second.parent.parent.name)
        self.assertIn(self.task_id,first.parent.parent.name)
        self.assertIn('nested-current',second.parent.parent.name)

if __name__=='__main__': unittest.main()
