from __future__ import annotations
import hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
PACKAGE=Path(__file__).resolve().parents[1]; SKILLS=PACKAGE.parents[1]; LOCAL=PACKAGE/'runtime'
for path in (SKILLS,LOCAL):
    if str(path) not in sys.path: sys.path.insert(0,str(path))
import execute, invoke, record
from common import index_tree_digest
from runtime.io import CommandError

class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name)/'repo'; self.inputs=Path(self.tmp.name)/'inputs'; self.inputs.mkdir(); subprocess.run(['git','init','-q','-b','main',str(self.repo)],check=True); self.git('config','user.name','Test'); self.git('config','user.email','test@example.invalid'); (self.repo/'.gitignore').write_text('.trellis/\n'); (self.repo/'base.txt').write_text('old\n'); self.git('add','.'); self.git('commit','-qm','old base'); self.old=self.git('rev-parse','HEAD'); (self.repo/'base.txt').write_text('new\n'); self.git('commit','-qam','new base'); self.new=self.git('rev-parse','HEAD'); self.git('switch','-qc','feature',self.old); (self.repo/'task.txt').write_text('task\n'); self.git('add','.'); self.git('commit','-qm','task'); self.head=self.git('rev-parse','HEAD'); self.task_ref='.trellis/tasks/current'; self.task_dir=self.repo/self.task_ref; self.task_dir.mkdir(parents=True); self.task_id='current-task'; self.write_identity()
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
    def continuity_gate(self,candidate_tree):
        gate=self.gate(); gate.update({'integration_impact':'continuity_review_required','typed_exit':'review_continuity_required','route_payload':{'candidate_tree_sha256':candidate_tree,'relevant_paths':['base.txt']},'summary':'Compatible post-review base delta requires a current reviewed-content identity.'}); return gate
    def candidate_tree(self):
        request=self.write('continuity-candidate.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[]})
        return execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)])['candidate_tree_sha256']
    def execute_reconciliation(self,profile):
        candidate_tree=self.candidate_tree(); public=self.public(profile)
        request={'task_ref':self.task_ref,'branch':'feature','prior_task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'branch_review_commit':self.head,'candidate_tree_sha256':candidate_tree,'commit_message':'chore(base): reconcile reviewed task'}
        receipt=execute.reconcile(PACKAGE,['--root',str(self.repo),'--request',str(self.write(profile+'-reconciliation-request.json',request))])
        return public,candidate_tree,receipt
    def add_uninitialized_gitlink(self):
        child = Path(self.tmp.name) / 'child'
        subprocess.run(['git', 'init', '-q', '-b', 'main', str(child)], check=True)
        def child_git(*args):
            return subprocess.run(
                ['git', *args], cwd=child, text=True, check=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            ).stdout.strip()
        child_git('config', 'user.name', 'Test')
        child_git('config', 'user.email', 'test@example.invalid')
        pointers = []
        for content in ('first\n', 'second\n'):
            (child / 'child.txt').write_text(content)
            child_git('add', 'child.txt')
            child_git('commit', '-qm', content.strip())
            pointers.append(child_git('rev-parse', 'HEAD'))
        self.git('config', '-f', '.gitmodules', 'submodule.child.path', 'vendor/child')
        self.git('config', '-f', '.gitmodules', 'submodule.child.url', str(child))
        self.git('add', '.gitmodules')
        self.git('update-index', '--add', '--cacheinfo', '160000', pointers[0], 'vendor/child')
        self.git('commit', '-qm', 'record uninitialized child pointer')
        self.head = self.git('rev-parse', 'HEAD')
        (self.repo / 'vendor/child').mkdir(parents=True)
        self.assertEqual([], list((self.repo / 'vendor/child').iterdir()))
        self.assertFalse((self.repo / '.git/modules').exists())
        self.assertEqual('', self.git('status', '--short'))
        self.assertEqual('', self.git('remote'))
        for oid in pointers:
            missing = subprocess.run(
                ['git', 'cat-file', '-e', oid], cwd=self.repo,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertNotEqual(0, missing.returncode)
        return pointers

    def candidate_state(self):
        return (
            self.git('rev-parse', 'HEAD'),
            (self.repo / '.git/index').read_bytes(),
            self.git('show-ref'),
            self.git('worktree', 'list', '--porcelain'),
        )

    def checked_gitlink_candidate(self, request, marker):
        before = self.candidate_state()
        with mock.patch.dict(os.environ, {'GIT_ALLOW_PROTOCOL': '', 'GIT_TERMINAL_PROMPT': '0'}):
            with mock.patch.object(subprocess, 'run', wraps=subprocess.run) as calls:
                try:
                    return execute.candidate(PACKAGE, [
                        '--root', str(self.repo), '--request', str(request),
                    ])
                except CommandError as error:
                    self.assertEqual('candidate_failed', error.code)
                    self.assertEqual('repository.index', error.field_path)
                    self.assertFalse(marker.exists())
                    raise
                finally:
                    self.assertEqual(before, self.candidate_state())
                    worktrees = [
                        Path(call.args[0][4]) for call in calls.call_args_list
                        if call.args[0][:3] == ['git', 'worktree', 'add']
                    ]
                    self.assertEqual(1, len(worktrees))
                    self.assertFalse(worktrees[0].exists())
                    self.assertFalse(worktrees[0].parent.exists())
                    for call in calls.call_args_list:
                        argv = call.args[0]
                        if argv[0] == 'git':
                            self.assertNotIn(argv[1], ('submodule', 'fetch', 'clone', 'pull', 'push', 'credential'))

    def test_gitlink_candidate_reaches_validation_and_preserves_task(self):
        self.add_uninitialized_gitlink()
        for exit_code in (0, 7):
            with self.subTest(exit_code=exit_code):
                marker = self.inputs / f'validation-{exit_code}.txt'
                command = [sys.executable, '-c',
                           'from pathlib import Path; import sys; '
                           'Path(sys.argv[1]).write_text(str(Path.cwd())); '
                           'raise SystemExit(int(sys.argv[2]))', str(marker), str(exit_code)]
                request = self.write(f'gitlink-{exit_code}.json', {
                    'task_head': self.head, 'new_base_head': self.new,
                    'validation_commands': [command],
                })
                result = self.checked_gitlink_candidate(request, marker)
                self.assertEqual('clean', result['merge_status'])
                self.assertEqual([], result['conflict_paths'])
                self.assertRegex(result['candidate_tree_sha256'], r'^[0-9a-f]{64}$')
                self.assertEqual([{'argv': command, 'exit_code': exit_code}], result['validations'])
                validation_cwd = Path(marker.read_text())
                self.assertEqual('worktree', validation_cwd.name)
                self.assertTrue(validation_cwd.parent.name.startswith('guru-base-candidate-'))
                self.assertFalse(validation_cwd.parent.exists())

    def test_gitlink_pointer_digest_is_exact_stable_and_needs_no_object(self):
        pointers = self.add_uninitialized_gitlink()
        blob_rows = []
        for path in ('.gitignore', '.gitmodules', 'base.txt', 'task.txt'):
            blob = subprocess.run(
                ['git', 'show', f':{path}'], cwd=self.repo,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            ).stdout
            blob_rows.append(path.encode() + b'\0' + hashlib.sha256(blob).hexdigest().encode() + b'\0')
        identities = []
        with mock.patch.dict(os.environ, {'GIT_ALLOW_PROTOCOL': '', 'GIT_TERMINAL_PROMPT': '0'}):
            with mock.patch.object(subprocess, 'run', wraps=subprocess.run) as calls:
                for oid in pointers:
                    self.git('update-index', '--cacheinfo', '160000', oid, 'vendor/child')
                    expected = hashlib.sha256(b''.join(blob_rows) +
                        b'vendor/child\0' + b'160000\0' + oid.encode('ascii') + b'\0').hexdigest()
                    actual = index_tree_digest(self.repo)
                    self.assertEqual(expected, actual)
                    self.assertEqual(actual, index_tree_digest(self.repo))
                    identities.append(actual)
                for call in calls.call_args_list:
                    argv = call.args[0]
                    if argv[:2] == ['git', 'cat-file']:
                        self.assertNotIn(argv[-1], pointers)
        self.assertNotEqual(*identities)
        self.assertEqual([], list((self.repo / 'vendor/child').iterdir()))
        self.assertFalse((self.repo / '.git/modules').exists())

    def test_blob_modes_retain_prior_digest_and_content_sensitivity(self):
        ordinary = self.repo / 'ordinary\tfile\n.txt'
        executable = self.repo / 'executable.sh'
        symlink = self.repo / 'link'
        ordinary.write_bytes(b'ordinary\0bytes\n')
        executable.write_bytes(b'#!/bin/sh\nexit 0\n')
        executable.chmod(0o755)
        symlink.symlink_to('missing-target')
        self.git('add', '--', ordinary.name, executable.name, symlink.name)
        self.git('update-index', '--chmod=+x', executable.name)

        def prior_digest():
            staged = subprocess.run(
                ['git', 'ls-files', '--stage', '-z'], cwd=self.repo,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            ).stdout
            rows = []
            modes = set()
            for entry in staged.split(b'\0'):
                if not entry:
                    continue
                metadata, path = entry.split(b'\t', 1)
                mode, oid, stage = metadata.split()
                self.assertEqual(b'0', stage)
                modes.add(mode)
                blob = subprocess.run(
                    ['git', 'cat-file', 'blob', oid.decode('ascii')], cwd=self.repo,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                ).stdout
                rows.append(path + b'\0' + hashlib.sha256(blob).hexdigest().encode() + b'\0')
            self.assertEqual({b'100644', b'100755', b'120000'}, modes)
            return hashlib.sha256(b''.join(rows)).hexdigest()

        previous = index_tree_digest(self.repo)
        self.assertEqual(prior_digest(), previous)
        for path in (ordinary, executable, symlink):
            with self.subTest(path=path.name):
                if path == symlink:
                    path.unlink()
                    path.symlink_to('another-missing-target')
                else:
                    path.write_bytes(path.read_bytes() + b'changed\n')
                self.git('add', '--', path.name)
                current = index_tree_digest(self.repo)
                self.assertEqual(prior_digest(), current)
                self.assertNotEqual(previous, current)
                previous = current
        # A link's index blob, not its filesystem target, owns its identity.
        (self.repo / 'another-missing-target').write_text('not indexed\n')
        self.assertEqual(previous, index_tree_digest(self.repo))

    def test_gitlink_reconciliation_retains_candidate_identity_and_parent_order(self):
        self.add_uninitialized_gitlink()
        observations = []
        def observe_index(repo):
            identity = index_tree_digest(repo)
            head = subprocess.run(
                ['git', 'rev-parse', 'HEAD'], cwd=repo, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
            ).stdout.strip()
            observations.append((repo, head, identity))
            return identity
        with mock.patch.dict(os.environ, {'GIT_ALLOW_PROTOCOL': '', 'GIT_TERMINAL_PROMPT': '0'}):
            with mock.patch.object(execute, 'index_tree_digest', side_effect=observe_index):
                public, candidate_tree, receipt = self.execute_reconciliation('post_branch_review')
            reconciled = receipt['reconciled_task_head']
            self.assertEqual(3, len(observations))
            self.assertEqual([candidate_tree] * 3, [row[2] for row in observations])
            self.assertEqual([self.new, self.head, reconciled], [row[1] for row in observations])
            self.assertEqual([self.repo.resolve()] * 2, [row[0].resolve() for row in observations[1:]])
            self.assertFalse(observations[0][0].parent.exists())
            self.assertEqual(candidate_tree, receipt['candidate_tree_sha256'])
            self.assertEqual([self.head, self.new], self.git('show', '-s', '--format=%P', reconciled).split())
            self.assertEqual('', self.git('status', '--short'))
            gate = self.continuity_gate(candidate_tree)
            owner = record.run(PACKAGE, {}, [
                '--root', str(self.repo), '--skill-input', str(self.write('gitlink-public.json', public)),
                '--semantic-review-file', str(self.write('gitlink-gate.json', gate)),
                '--typed-exit', 'review_continuity_required',
                '--reconciliation-result', str(self.write('gitlink-receipt.json', receipt)),
            ])
            output = invoke.run(PACKAGE, {}, [
                '--root', str(self.repo), '--invocation', str(self.write('gitlink-envelope.json', {
                    'public_input': public, 'owner_result': owner,
                })),
            ])
            self.assertEqual(reconciled, output['task_head'])
            self.assertEqual(candidate_tree, output['candidate_tree_sha256'])
            self.assertEqual('review_continuity_required', output['exit_id'])
    def test_guard_unchanged_and_new_pair_write_nothing(self):
        before=self.runtime_snapshot(); public=self.public(); path=self.write('public.json',public); self.assertEqual('new_pair',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status']); public['old_base_head']=self.new; path=self.write('same.json',public); self.assertEqual('unchanged',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(path)])['status']); self.assertEqual(before,self.runtime_snapshot())
    def test_all_boundaries_unchanged_are_zero_write_and_need_no_review_identity(self):
        for profile in ('post_plan','post_check','post_commit','post_branch_review','post_publication','finalizer_base_mismatch'):
            public=self.public(profile); public['old_base_head']=self.new
            result=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write(profile+'.json',public))])
            self.assertEqual('unchanged',result['status'],profile)
        self.assertNotIn('branch_review_commit',self.public('post_commit'))
    def test_post_plan_accepts_planning_before_activation_but_later_boundaries_do_not(self):
        self.write_identity(status='planning')
        post_plan=self.public('post_plan'); post_plan['old_base_head']=self.new
        self.assertEqual('unchanged',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write('planning-post-plan.json',post_plan))])['status'])
        post_plan['old_base_head']=self.old
        public_path=self.write('planning-new-pair.json',post_plan); gate_path=self.write('planning-gate.json',self.gate())
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled'])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('planning-envelope.json',{'public_input':post_plan,'owner_result':owner}))])
        self.assertEqual('task_activation',output['resume_target'])
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled'])
        guarded=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(public_path)])
        self.assertEqual('current_pair',guarded['status'])
        self.assertEqual(owner['typed_output'],guarded['typed_output'])
        post_check=self.public('post_check'); post_check['old_base_head']=self.new
        with self.assertRaises(CommandError) as raised:
            execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write('planning-post-check.json',post_check))])
        self.assertEqual('stale_identity',raised.exception.code)
    def test_unrelated_post_plan_base_delta_preserves_task_activation(self):
        self.write_identity(status='planning')
        public=self.public('post_plan'); public_path=self.write('unrelated-post-plan.json',public)
        gate=self.gate(); gate.update({'key_delta_refs':['unrelated-base-only.txt'],'validation_evidence':['base-only delta is unrelated and candidate validations passed'],'summary':'Only the integration clock advanced; authority and approved planning assumptions remain current.'})
        gate_path=self.write('unrelated-post-plan-gate.json',gate)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled'])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('unrelated-post-plan-envelope.json',{'public_input':public,'owner_result':owner}))])
        self.assertEqual('reconciled',output['exit_id'])
        self.assertEqual('task_activation',output['resume_target'])
    def test_real_planning_authority_change_remains_planning_stale(self):
        self.write_identity(status='planning')
        public=self.public('post_plan'); public_path=self.write('authority-change-post-plan.json',public)
        gate=self.gate(); gate.update({'authority_impact':'changed','task_content_impact':'planning_stale','integration_impact':'compatible','summary':'Live Issue authority invalidated an approved planning assumption.','typed_exit':'planning_stale','route_payload':{'reason_refs':['live-issue-authority-changed']}})
        gate_path=self.write('authority-change-post-plan-gate.json',gate)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','planning_stale'])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('authority-change-post-plan-envelope.json',{'public_input':public,'owner_result':owner}))])
        self.assertEqual({'exit_id':'planning_stale','task_ref':self.task_ref,'reason_refs':['live-issue-authority-changed']},output)
    def test_multiple_base_commits_form_one_cumulative_pair(self):
        self.git('switch','main'); (self.repo/'second.txt').write_text('second\n'); self.git('add','second.txt'); self.git('commit','-qm','second base advance'); newest=self.git('rev-parse','HEAD'); self.git('switch','feature')
        public=self.public(); public['selected_base_ref']=newest; public['new_base_head']=newest
        result=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write('cumulative.json',public))])
        self.assertEqual('new_pair',result['status']); self.assertEqual(self.old,result['old_base_head']); self.assertEqual(newest,result['new_base_head'])
    def test_candidate_is_clean_and_leaves_no_worktree(self):
        request=self.write('request.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[['git','status','--short']]}); result=execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)]); self.assertEqual('clean',result['merge_status']); self.assertRegex(result['candidate_tree_sha256'],r'^[0-9a-f]{64}$'); self.assertEqual([],result['conflict_paths']); self.assertNotIn('guru-base-candidate-',self.git('worktree','list'))
    def test_candidate_routes_python_validation_through_managed_interpreter(self):
        request=self.write('python-request.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[['python3','-c','import sys; raise SystemExit(0 if sys.executable else 1)']]}); result=execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)]); self.assertEqual(sys.executable,result['validations'][0]['argv'][0]); self.assertEqual(0,result['validations'][0]['exit_code'])
    def test_post_review_profiles_create_one_local_commit_and_publish_current_head(self):
        for profile in ('post_branch_review','post_publication','finalizer_base_mismatch'):
            with self.subTest(profile=profile):
                public,candidate_tree,receipt=self.execute_reconciliation(profile)
                reconciled=receipt['reconciled_task_head']; self.assertEqual([self.head,self.new],self.git('show','-s','--format=%P',reconciled).split()); self.assertEqual('',self.git('status','--short'))
                gate=self.continuity_gate(candidate_tree); owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(self.write(profile+'-public.json',public)),'--semantic-review-file',str(self.write(profile+'-gate.json',gate)),'--typed-exit','review_continuity_required','--reconciliation-result',str(self.write(profile+'-receipt.json',receipt))])
                output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write(profile+'-envelope.json',{'public_input':public,'owner_result':owner}))])
                self.assertEqual('review_continuity_required',output['exit_id']); self.assertEqual(reconciled,output['task_head']); self.assertEqual(self.head,output['branch_review_commit']); self.assertEqual(candidate_tree,output['candidate_tree_sha256'])
                self.git('reset','--hard',self.head)
    def test_post_review_current_pair_recovers_after_reconciliation_commit(self):
        public,candidate_tree,receipt=self.execute_reconciliation('finalizer_base_mismatch')
        gate=self.continuity_gate(candidate_tree)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(self.write('recovery-public.json',public)),'--semantic-review-file',str(self.write('recovery-gate.json',gate)),'--typed-exit','review_continuity_required','--reconciliation-result',str(self.write('recovery-receipt.json',receipt))])
        guarded=execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write('recovery-guard.json',public))])
        self.assertEqual('current_pair',guarded['status'])
        self.assertEqual(owner['typed_output'],guarded['typed_output'])
        self.assertEqual(receipt['reconciled_task_head'],guarded['typed_output']['task_head'])
        self.assertEqual('blocked',execute.guard(PACKAGE,['--root',str(self.repo),'--input',str(self.write('recovery-second-guard.json',public))])['status'])
    def test_reconciliation_stale_dirty_and_candidate_mismatch_fail_without_commit(self):
        candidate_tree=self.candidate_tree(); base={'task_ref':self.task_ref,'branch':'feature','prior_task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'branch_review_commit':self.head,'candidate_tree_sha256':candidate_tree,'commit_message':'chore(base): reconcile reviewed task'}
        cases=[('stale-head',{**base,'prior_task_head':self.old},None),('candidate',{**base,'candidate_tree_sha256':'f'*64},None),('dirty',base,lambda:(self.repo/'dirty.txt').write_text('dirty\n'))]
        for name,request,mutate in cases:
            with self.subTest(name=name):
                if mutate: mutate()
                with self.assertRaises(CommandError): execute.reconcile(PACKAGE,['--root',str(self.repo),'--request',str(self.write(name+'-request.json',request))])
                self.assertEqual(self.head,self.git('rev-parse','HEAD'))
                if name=='dirty': (self.repo/'dirty.txt').unlink()
                self.assertNotEqual(0,subprocess.run(['git','rev-parse','--verify','--quiet','MERGE_HEAD'],cwd=self.repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode)
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
