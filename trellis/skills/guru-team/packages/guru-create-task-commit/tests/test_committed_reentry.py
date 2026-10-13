"""Delivery migration of #530's real Git/public-wrapper clean reentry checks.

Fixture semantic authoring never claims independent AI approval. Five-blob
migration is exercised by test_delivery_migration, not precommitted new paths.
"""
from __future__ import annotations
import importlib.util
import hashlib
import json
import shutil
import subprocess
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]


class CommittedReentryTest(unittest.TestCase):
    def setUp(self):
        # Reuse public API setup, without duplicating schema or discovering its
        # TestCase here. Product calls below remain the real public wrappers.
        spec = importlib.util.spec_from_file_location('taskcommit_delivery_fixture', SKILLS / 'packages/guru-check-task/tests/test_delivery_flow.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.fixture = module.DeliveryFlow()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.repo, self.key, self.task_ref = self.fixture.repo, self.fixture.key, self.fixture.task_ref
        self.projection = self.fixture.projection

    def git(self, *args):
        return self.fixture.git(*args).strip()

    def call(self, skill, script, *args, ok=True):
        return self.fixture.wrapper(skill, script, *args, success=ok)

    def write(self, name, value):
        return self.fixture.write(name, value)

    def phase2(self, mode='workflow'):
        self.fixture.head = self.git('rev-parse', 'HEAD')
        package = SKILLS / 'packages/guru-check-task'
        spec = importlib.util.spec_from_file_location('reentry_check_identity', package / 'runtime/common.py')
        common = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(common)
        owner = json.loads((package / 'examples/phase2-check.json').read_text())
        owner.update(mode=mode, task_ref=self.task_ref, phase2_capture_commit=self.fixture.head,
                     reviewed_content_sha256=common.content_identity(self.repo), reviewed_paths=['app.txt'], candidate_classifications=[])
        public = {'profile':'delivery_initial_check','mode':mode,'task_ref':self.task_ref,'delivery_key':self.key,
                  'source_exit':'implementation_complete','planning_accepted_result_id':'planning:flow'}
        return self.call('guru-check-task','invoke.sh','--input',self.write('check.json',public),'--owner-result',self.write('check-owner.json',owner))

    def restart_implementation(self):
        from runtime.delivery_projection.gates import rework
        from runtime.delivery_projection.adapter import authority_ref
        delivery = self.projection.resolve(self.key)
        role = 'full_review' if delivery['phase'] == 'reviewing' else 'check'
        rework(self.projection,self.key,role,'implementation',authority_ref(self.repo/'requirements.md',self.repo),['check','full_review','readiness'])
        self.projection.begin_check(self.key,self.projection.candidate(['app.txt'],head_ref=self.git('rev-parse','HEAD'),base_ref=self.git('rev-parse','main')))

    def reentry(self, passed, status='passed', ok=True, mode='workflow', extra=()):
        public={'profile':'delivery_committed_reentry','mode':mode,'task_ref':self.task_ref,'delivery_key':self.key,'check_result_id':passed['check_result_id']}
        owner={'status':status,'summary':'Fixture current clean candidate.','evidence':['Actual current candidate, planning and full range.']}
        return self.call(PACKAGE.name,'invoke.sh','--input',self.write('reentry.json',public),'--owner-result',self.write('reentry-owner.json',owner),*extra,ok=ok)

    def prepare(self, passed, ok=True):
        from runtime.reviewed_content import reviewed_content_metadata_path
        paths=subprocess.run(['git','status','--porcelain=v1','--untracked-files=all'],cwd=self.repo,capture_output=True,text=True,check=True).stdout.splitlines()
        authoring={'path_classifications':[{'path':row[3:],'category':'unrelated-preserved' if reviewed_content_metadata_path(row[3:]) else 'task-reviewed','reason':'Preserve derived public metadata; commit only genuine content.','coverage_source':'Current public Check'} for row in paths],
                   'message':{'type':'fix','scope':'fixture','summary':'验证Delivery增量','background':'保留clean候选接续。','changes':'提交真实增量。','boundaries':'只作用临时仓库。','validations':'运行真实wrapper。'},
                   'ai_review':{'status':'passed','summary':'Fixture-only authoring.','evidence':['Actual dirty snapshot.']}}
        public={'profile':'delivery_initial_commit','mode':'workflow','task_ref':self.task_ref,'delivery_key':self.key,'source_exit':'passed','check_result_id':passed['check_result_id']}
        return self.call(PACKAGE.name,'prepare-task-commit.sh','--input',self.write('dirty-input.json',public),'--candidate-json',self.write('dirty-owner.json',authoring),ok=ok)

    def guard(self, profile):
        public={'profile':'delivery_'+profile,'mode':'workflow','task_ref':self.task_ref,'delivery_key':self.key,'task_head':self.git('rev-parse','HEAD'),
                'selected_base_ref':'main','resume_target':'branch_review' if profile=='post_commit' else 'task_commit'}
        return self.call('guru-reconcile-task-base','guard-task-base-pair.sh','--input',self.write('guard.json',public))

    def reconcile(self):
        # Ordinary base integration needs tracked current public metadata.
        # This fixture maintenance commit is not a repeated business candidate.
        self.git('add',self.task_ref); self.git('commit','-qm','persist current public fixture facts')
        prior,old_base=self.git('rev-parse','HEAD'),self.git('rev-parse','main')
        self.git('switch','main'); (self.repo/'base-only.txt').write_text('evolved base\n')
        self.git('add','base-only.txt'); self.git('commit','-qm','advance base')
        new_base=self.git('rev-parse','HEAD'); self.git('switch','feat/flow')
        self.assertEqual('new_pair',self.guard('post_commit')['status'])
        skill='guru-reconcile-task-base'
        candidate=self.call(skill,'execute-base-candidate.sh','--request',self.write('candidate.json',{'task_head':prior,'new_base_head':new_base,'validation_commands':[]}))
        public={'profile':'delivery_post_commit','mode':'workflow','task_ref':self.task_ref,'delivery_key':self.key,'task_head':prior,'selected_base_ref':'main','resume_target':'branch_review'}
        request={'profile':public['profile'],'task_ref':self.task_ref,'delivery_key':self.key,'branch':'feat/flow','prior_task_head':prior,'selected_base_ref':'main',
                 'old_base_head':old_base,'new_base_head':new_base,'resume_target':'branch_review','candidate_tree_sha256':candidate['candidate_tree_sha256'],'commit_message':'chore(base): 整合临时基线'}
        result=self.call(skill,'execute-base-reconciliation.sh','--request',self.write('reconcile.json',request))
        gate={'authority_impact':'unchanged','task_content_impact':'unchanged','integration_impact':'compatible','reviewed_scope':['authority','planning','delta'],
              'key_delta_refs':['base-only.txt'],'validation_evidence':['Actual clean candidate.'],'unverified_boundaries':[],'summary':'Fixture compatible base integration.',
              'typed_exit':'reconciled','route_payload':{'candidate_tree_sha256':candidate['candidate_tree_sha256'],'relevant_paths':['base-only.txt']}}
        recorded=self.call(skill,'record-base-reconciliation.sh','--skill-input',self.write('reconcile-public.json',public),'--semantic-review-file',self.write('reconcile-gate.json',gate),
                           '--typed-exit','reconciled','--reconciliation-result',self.write('reconcile-result.json',result))
        output=self.call(skill,'invoke.sh','--invocation',self.write('reconcile-envelope.json',{'public_input':public,'owner_result':recorded}))
        self.assertEqual('reconciled',output['exit_id']); self.assertEqual('phase2',output['resume_target'])
        self.restart_implementation()

    def snapshot(self):
        return tuple(self.git(*args) for args in [('rev-parse','HEAD','HEAD^{tree}'),('ls-files','--stage'),('status','--porcelain=v1','--untracked-files=all'),('rev-list','--count','HEAD'),('reflog','--format=%H')])

    def install_fixture_packages(self, *skills):
        """Copy runtime assets for wrapper tests, not installer acceptance."""
        installed = self.repo / '.trellis/guru-team'
        # Fixture Git exclude keeps copied tools out of reviewed business data.
        with (self.repo / '.git/info/exclude').open('a') as stream:
            stream.write('\n.trellis/guru-team/\n')
        shutil.copytree(SKILLS / 'runtime', installed / 'runtime', dirs_exist_ok=True)
        shutil.copytree(SKILLS / 'schemas', installed / 'skills/schemas', dirs_exist_ok=True)
        for skill in skills:
            shutil.copytree(SKILLS / 'packages' / skill, installed / 'skills/packages' / skill, dirs_exist_ok=True)
        source_repo = next(parent for parent in PACKAGE.parents if (parent / '.git').exists())
        common = subprocess.run(['git','rev-parse','--path-format=absolute','--git-common-dir'], cwd=source_repo, capture_output=True, text=True, check=True).stdout.strip()
        pointer = self.repo / '.git/guru-team/python/active.json'
        pointer.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(common) / 'guru-team/python/active.json', pointer)
        return installed

    def architecture(self, committed):
        package = SKILLS / 'packages/guru-maintain-architecture-baseline'
        installed = self.install_fixture_packages(package.name)
        public = json.loads((package / 'examples/public-input-impact.json').read_text())
        constitution = '.trellis/.runtime/fixture-constitution.md'
        (self.repo / constitution).write_text('Current fixture design constitution.\n')
        public['constitution']['authority_locator'] = constitution
        public.update(schema_version='delivery-1.0', profile='delivery_task_impact_sync',
                      delivery_key=self.key, planning_root=self.projection.resolve(self.key)['planning_root'],
                      source_exit=committed['exit_id'], stage='branch_review', task_locator=self.task_ref,
                      freshness_identity=committed['branch_review_commit'], committed_range={
                          'base_ref':committed['base_ref'], 'base_head':self.git('rev-parse',committed['base_ref']),
                          'review_head':committed['branch_review_commit']})
        owner = {key:public[key] for key in ('schema_version','profile','mode','continuation_id','stage','task_locator',
                                            'baseline','constitution','project_contract','freshness_identity','delivery_key','planning_root')}
        owner.update(input_sha256=hashlib.sha256(json.dumps(public,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                     typed_exit='baseline_current', consumer={'kind':'workflow','id':'guru-architecture-baseline-current-router'},
                     baseline_identity=public['baseline']['identity'], constitution_identity=public['constitution']['identity'],
                     impact_kind='no_architecture_impact', impact_reason='Fixture changes application text, with all architecture boundaries retained.',
                     promotion_state='no_change', ai_review_gate={'status':'passed','reviewed_scope':'Complete fixture committed range.',
                         'evidence_summary':'Fixture-only authoring, not independent AI assessment.','findings':[], 'conclusion':'Fixture no-impact projection.'})
        result = subprocess.run(['bash',str(installed/'skills/packages'/package.name/'scripts/invoke.sh'),'--invocation','-'],
                                input=json.dumps({'public_input':public,'owner_result':owner}),cwd=self.repo,capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
        return json.loads(result.stdout)

    def test_real_reconcile_fresh_check_and_first_full_review(self):
        self.phase2(); self.reconcile(); passed=self.phase2()
        self.assertEqual('unchanged',self.guard('post_check')['status'])
        # No manufactured empty commit: metadata-only dirty does not suffice.
        failed=self.prepare(passed,ok=False)
        self.assertEqual('schema_mismatch',failed['code']); self.assertIn('exact_stage_paths',failed['field_path'])
        marker=self.repo/'.git/reentry-hook-ran'; hook=self.repo/'.git/hooks/pre-commit'
        hook.write_text(f"#!/bin/sh\ntouch '{marker}'\nexit 1\n"); hook.chmod(0o755)
        before=self.snapshot(); output=self.reentry(passed)
        self.assertEqual(before,self.snapshot()); self.assertFalse(marker.exists())
        self.assertEqual('committed',output['exit_id']); self.assertEqual('unchanged',self.guard('post_commit')['status'])
        self.assertIsNone(self.projection.resolve(self.key)['results']['full_review'])
        architecture = self.architecture(output)
        self.assertEqual('baseline_current',architecture['exit_id'])
        self.assertEqual(output['branch_review_commit'],architecture['freshness_identity'])
        self.assertEqual(self.key,architecture['delivery_key'])
        self.assertEqual(before,self.snapshot())
        self.assertEqual('passed',self.fixture.full_review(passed)['exit_id'])
        self.assertEqual(output['branch_review_commit'],self.git('rev-parse','HEAD'))

    def test_clean_stdout_loss_keeps_public_check_and_same_dto(self):
        passed=self.phase2(); before=self.snapshot(); output=self.reentry(passed)
        self.assertEqual(output,self.reentry(passed)); self.assertEqual(before,self.snapshot())
        self.assertEqual(passed['check_result_id'],self.projection.resolve(self.key)['results']['check']['result_id'])
        self.assertFalse(list((self.repo/'.trellis/.runtime/guru-team/task-commit-results').rglob('*.json')))

    def test_dirty_increment_exact_transaction_recovers_once(self):
        passed=self.phase2(); (self.repo/'app.txt').write_text('next genuine increment\n')
        self.assertEqual('stale_identity',self.reentry(passed,ok=False)['code'])
        self.restart_implementation(); prepared=self.prepare(self.phase2()); before=int(self.git('rev-list','--count','HEAD'))
        args=('--candidate-artifact',prepared['candidate_artifact']); output=self.call(PACKAGE.name,'invoke.sh',*args)
        self.assertEqual(output,self.call(PACKAGE.name,'invoke.sh',*args)); self.assertEqual(before+1,int(self.git('rev-list','--count','HEAD')))
        self.restart_implementation(); self.assertEqual(output['branch_review_commit'],self.reentry(self.phase2())['branch_review_commit'])

    def test_normal_mode_base_and_checkout_changes_require_reentry(self):
        passed=self.phase2(); (self.repo/'app.txt').chmod(0o755); self.git('commit','-qam','change executable mode')
        self.assertEqual('stale_identity',self.reentry(passed,ok=False)['code'])
        self.restart_implementation(); passed=self.phase2()
        self.git('add',self.task_ref); self.git('commit','-qm','persist actual public facts before checkout')
        self.git('switch','main'); (self.repo/'base-only.txt').write_text('base advance\n'); self.git('add','base-only.txt'); self.git('commit','-qm','advance'); self.git('switch','feat/flow')
        self.assertEqual('stale_identity',self.reentry(passed,ok=False)['code'])
        self.git('switch','-qc','feat/other'); self.assertEqual('stale_identity',self.reentry(passed,ok=False)['code'])

    def test_standalone_recovers_without_legacy_checkpoint(self):
        passed=self.phase2(mode='standalone'); before=self.snapshot(); output=self.reentry(passed,mode='standalone')
        self.assertEqual(output,self.reentry(passed,mode='standalone')); self.assertEqual(before,self.snapshot())

    def test_missing_selected_base_has_explicit_diagnostic(self):
        passed = self.phase2()
        task_file = self.repo / self.task_ref / 'task.json'
        record = json.loads(task_file.read_text())
        record['base_branch'] = None  # Normal incomplete old installation metadata.
        task_file.write_text(json.dumps(record))
        before = self.snapshot()
        rejected = self.reentry(passed,ok=False)
        self.assertEqual('stale_identity',rejected['code'])
        self.assertEqual('base_branch',rejected['field_path'])
        self.assertEqual(before,self.snapshot())

    def test_no_task_range_rejects_without_mutation(self):
        passed=self.phase2(); self.git('branch','-f','main','HEAD')
        before=self.snapshot(); self.assertEqual('stale_identity',self.reentry(passed,ok=False)['code']); self.assertEqual(before,self.snapshot())

    def test_nonpass_conflicting_arguments_and_real_merge(self):
        passed=self.phase2(); before=self.snapshot()
        self.assertEqual('blocked',self.reentry(passed,status='blocked')['exit_id']); self.assertEqual('revision-required',self.reentry(passed,status='revision-required')['exit_id'])
        self.assertEqual(before,self.snapshot()); self.assertEqual('conflicting_arguments',self.reentry(passed,ok=False,extra=('--invocation','-'))['code'])
        self.git('add',self.task_ref); self.git('commit','-qm','persist actual public facts')
        self.restart_implementation(); passed=self.phase2(); self.git('add',self.task_ref); self.git('commit','-qm','persist actual fresh Check')
        self.git('switch','main'); (self.repo/'base-only.txt').write_text('merge base\n'); self.git('add','base-only.txt'); self.git('commit','-qm','advance')
        self.git('switch','feat/flow'); self.git('merge','--no-commit','--no-ff','main')
        self.assertEqual('stale_identity',self.reentry(passed,ok=False)['code'])

    def test_native_boundary_consumes_actual_delivery_public_outputs(self):
        from adapters.eval.native_adapter import start_public_runtime_boundary
        passed = self.phase2()
        expected = self.reentry(passed)
        installed = self.install_fixture_packages(PACKAGE.name)
        package = installed / 'skills/packages' / PACKAGE.name
        target = installed / 'scripts/bash/run-skill-command.sh'
        execution_root = self.repo / '.trellis/.runtime/native-boundary'
        execution_root.mkdir(parents=True)
        projection = execution_root / 'model-package'
        before = self.snapshot()
        boundary, thread, stop = start_public_runtime_boundary(execution_root, target, package, projection, projection / 'scripts/invoke.sh', {})
        try:
            args = ['--package-root',str(projection),'--input',self.write('native-input.json',{
                'profile':'delivery_committed_reentry','mode':'workflow','task_ref':self.task_ref,
                'delivery_key':self.key,'check_result_id':passed['check_result_id']}),
                '--owner-result',self.write('native-owner.json',{'status':'passed','summary':'Fixture current clean candidate.','evidence':['Actual public Check.']})]
            result = subprocess.run([str(boundary),*args],cwd=self.repo,capture_output=True,text=True,timeout=30)
            self.assertEqual(0,result.returncode,result.stdout+result.stderr)
            self.assertEqual(expected,json.loads(result.stdout))
            self.assertEqual(before,self.snapshot())
        finally:
            stop.set(); thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
