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
        self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name)/'repo'; self.inputs=Path(self.tmp.name)/'inputs'; self.inputs.mkdir(); subprocess.run(['git','init','-q','-b','main',str(self.repo)],check=True); self.git('config','user.name','Test'); self.git('config','user.email','test@example.invalid'); (self.repo/'base.txt').write_text('old\n'); self.git('add','.'); self.git('commit','-qm','old base'); self.old=self.git('rev-parse','HEAD'); (self.repo/'base.txt').write_text('new\n'); self.git('commit','-qam','new base'); self.new=self.git('rev-parse','HEAD'); self.git('switch','-qc','feature',self.old); (self.repo/'task.txt').write_text('task\n'); self.git('add','.'); self.git('commit','-qm','task'); self.head=self.git('rev-parse','HEAD')
    def tearDown(self): self.tmp.cleanup()
    def git(self,*args): return subprocess.run(['git',*args],cwd=self.repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()
    def write(self,name,value): path=self.inputs/name; path.write_text(json.dumps(value)); return path
    def public(self, profile='post_check'):
        targets={'post_plan':'task_activation','post_check':'task_commit','post_commit':'branch_review','post_branch_review':'publication_review','post_publication':'task_finalization','finalizer_base_mismatch':'finalization_resume'}
        value={'profile':profile,'mode':'workflow','task_ref':'.trellis/tasks/current','task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'resume_target':targets[profile]}
        if profile in {'post_branch_review','post_publication','finalizer_base_mismatch'}: value['branch_review_commit']=self.head
        return value
    def gate(self): return {'authority_impact':'unchanged','task_content_impact':'unchanged','integration_impact':'compatible','reviewed_scope':['authority','planning','delta'],'key_delta_refs':['base.txt'],'validation_evidence':['candidate clean'],'unverified_boundaries':[],'summary':'Compatible.','typed_exit':'reconciled','route_payload':{}}
    def test_guard_unchanged_and_new_pair_write_nothing(self):
        public=self.public(); path=self.write('public.json',public); self.assertEqual('new_pair',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status']); public['old_base_head']=self.new; path=self.write('same.json',public); self.assertEqual('unchanged',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status']); self.assertFalse((self.repo/'.trellis').exists())
    def test_all_boundaries_unchanged_are_zero_write_and_need_no_review_identity(self):
        for profile in ('post_plan','post_check','post_commit','post_branch_review','post_publication','finalizer_base_mismatch'):
            public=self.public(profile); public['old_base_head']=self.new
            result=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write(profile+'.json',public))])
            self.assertEqual('unchanged',result['status'],profile)
        self.assertNotIn('branch_review_commit',self.public('post_commit'))
        self.assertFalse((self.repo/'.trellis').exists())
    def test_multiple_base_commits_form_one_cumulative_pair(self):
        self.git('switch','main'); (self.repo/'second.txt').write_text('second\n'); self.git('add','.'); self.git('commit','-qm','second base advance'); newest=self.git('rev-parse','HEAD'); self.git('switch','feature')
        public=self.public(); public['selected_base_ref']=newest; public['new_base_head']=newest
        result=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write('cumulative.json',public))])
        self.assertEqual('new_pair',result['status']); self.assertEqual(self.old,result['old_base_head']); self.assertEqual(newest,result['new_base_head'])
    def test_candidate_is_clean_and_leaves_no_worktree(self):
        request=self.write('request.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[['git','status','--short']]}); result=execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)]); self.assertEqual('clean',result['merge_status']); self.assertRegex(result['candidate_tree_sha256'],r'^[0-9a-f]{64}$'); self.assertEqual([],result['conflict_paths']); self.assertNotIn('guru-base-candidate-',self.git('worktree','list'))
    def test_record_invoke_consumes_checkpoint_once(self):
        public=self.public(); pi=self.write('public.json',public); gate=self.write('gate.json',self.gate()); result=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gate),'--typed-exit','reconciled']); envelope=self.write('envelope.json',{'public_input':public,'owner_result':result}); output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)]); self.assertEqual('reconciled',output['exit_id']); checkpoint=self.repo/'.trellis/.runtime/guru-team/owner-checkpoints/current/guru-reconcile-task-base/base-reconciliation.json'; self.assertFalse(checkpoint.exists())
    def test_current_pair_is_reused_once_then_retires(self):
        public=self.public(); pi=self.write('reuse-public.json',public); gate=self.write('reuse-gate.json',self.gate()); result=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gate),'--typed-exit','reconciled'])
        self.assertEqual('current_pair',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(pi)])['status'])
        envelope=self.write('reuse-envelope.json',{'public_input':public,'owner_result':result}); self.assertEqual('task_commit',invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])['resume_target'])
        self.assertEqual('new_pair',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(pi)])['status'])
    def test_132_161_replay_preserves_review_head_and_resumes_finalizer(self):
        public=self.public('finalizer_base_mismatch'); pi=self.write('historical-finalizer.json',public); gate=self.gate(); gate['reviewed_scope'].append('historical #132/#161 base-only stale route'); gp=self.write('historical-gate.json',gate)
        result=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gp),'--typed-exit','reconciled']); envelope=self.write('historical-envelope.json',{'public_input':public,'owner_result':result}); output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])
        self.assertEqual('finalization_resume',output['resume_target']); self.assertEqual(self.head,public['branch_review_commit']); self.assertNotIn('branch_review_commit',output)
    def test_history_rewrite_blocks(self):
        public=self.public(); public['old_base_head']=self.head; path=self.write('bad.json',public); self.assertEqual('blocked',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status'])

if __name__=='__main__': unittest.main()
