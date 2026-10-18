from __future__ import annotations
import hashlib, json, os, stat, subprocess, sys, tempfile, unittest
from pathlib import Path
from unittest import mock
PACKAGE=Path(__file__).resolve().parents[1]; SKILLS=PACKAGE.parents[1]; LOCAL=PACKAGE/'runtime'
for path in (SKILLS,LOCAL):
    if str(path) not in sys.path: sys.path.insert(0,str(path))
import common, execute, invoke, record
from common import index_tree_digest
from runtime.io import CommandError
from runtime.delivery_projection.tests.upstream_fixture import install_common, public_task
from runtime.delivery_projection import DeliveryProjection, authority_ref
from runtime.delivery_projection.gates import record_gate, rework
from runtime.delivery_projection.tests.test_installed_projection import DECLARATION
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository

class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.repo=Path(self.tmp.name)/'repo'; self.inputs=Path(self.tmp.name)/'inputs'; self.inputs.mkdir(); subprocess.run(['git','init','-q','-b','main',str(self.repo)],check=True); self.git('config','user.name','Test'); self.git('config','user.email','test@example.invalid'); (self.repo/'.gitignore').write_text('.trellis/\n'); (self.repo/'base.txt').write_text('old\n'); self.git('add','.'); self.git('commit','-qm','old base'); self.old=self.git('rev-parse','HEAD'); (self.repo/'base.txt').write_text('new\n'); self.git('commit','-qam','new base'); self.new=self.git('rev-parse','HEAD'); self.git('switch','-qc','feature',self.old); (self.repo/'task.txt').write_text('task\n'); self.git('add','.'); self.git('commit','-qm','task'); self.head=self.git('rev-parse','HEAD'); self.task_ref='.trellis/tasks/current'; self.task_dir=self.repo/self.task_ref; self.task_dir.mkdir(parents=True); self.task_id='current-task'; self.write_identity()
    def tearDown(self): self.tmp.cleanup()
    def git(self,*args): return subprocess.run(['git',*args],cwd=self.repo,text=True,stdout=subprocess.PIPE,check=True).stdout.strip()
    def write(self,name,value): path=self.inputs/name; path.write_text(json.dumps(value)); return path
    def write_identity(self,status='in_progress',branch='feature',task_ref=None,task_id=None):
        task_ref=task_ref or self.task_ref; task_id=task_id or self.task_id; task_dir=self.repo/task_ref; task_dir.mkdir(parents=True,exist_ok=True)
        install_common(self.repo)
        (self.repo/'.trellis/workflow.md').write_text('[trellis-runtime-contract]\n'+json.dumps(DECLARATION)+'\n[/trellis-runtime-contract]\n')
        (task_dir/'task.json').write_text(json.dumps(public_task({
            'id':task_id,'name':task_id,'lifecycle_generation':0,
            'source':{'kind':'no_issue'},'title':'Base reconciliation fixture',
            'description':'Current task and unchanged/evolved base pair.',
            'status':status,'dev_type':None,'scope':'local fixture','package':None,
            'priority':'P2','createdAt':'2026-10-09','completedAt':None,
            'base_branch':'main','worktree_path':None,'commit':None,'pr_url':None,
            'children':[],'parent':None,'relatedFiles':[],'notes':'','meta':{},
        })))
        projection=DeliveryProjection(self.repo,task_ref)
        (task_dir/'prd.md').write_text('整体 Task scope\n')
        scope=authority_ref(task_dir/'prd.md',self.repo); projection.scope(scope)
        delivery_key={'task_id':task_id,'lifecycle_generation':0,'delivery_id':'8ec361f1-a63e-4d75-819f-1e9b6a410871'}
        projection.apply({'api_version':'1.0','operation':'create_delivery','key':delivery_key,
                          'owner_role':'creation','owner_id':'guru-create-delivery','profile':'pull_request',
                          'scope_ref':{'authority':scope,'anchors':['本次候选']}})
        if task_id==self.task_id:self.delivery_key=delivery_key
        if status=='done':
            metadata=__import__('json').loads((task_dir/'task.json').read_text()); metadata['schema_version']='1.0'
            (task_dir/'task.json').write_text(json.dumps(metadata))
        store=BranchBindingStore(inspect_repository(self.repo)); key=TaskLifecycleKey(task_id,0)
        binding=store.read(key)
        if binding is None:
            store.establish(key,branch)
        elif binding.branch_name != branch:
            path=store.path_for(key); data=binding.as_dict(); data['branch_name']=branch; path.write_text(json.dumps(data))
    def runtime_snapshot(self):
        root=self.repo/'.trellis/.runtime'; return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
    def public(self, profile='delivery_post_check'):
        targets={'delivery_post_plan':'delivery_activation','delivery_post_check':'task_commit','delivery_post_commit':'branch_review','delivery_post_branch_review':'publication_review','delivery_post_publication':'delivery_publication','delivery_finalizer_base_mismatch':'finalization_resume'}
        value={'profile':profile,'mode':'workflow','task_ref':self.task_ref,'delivery_key':self.delivery_key,'task_head':self.head,'selected_base_ref':self.new,'resume_target':targets[profile]}
        if profile in {'delivery_post_branch_review','delivery_post_publication','delivery_finalizer_base_mismatch'}:
            value.update({'old_base_head':self.old,'new_base_head':self.new,'branch_review_commit':self.head})
        return value
    def gate(self, candidate_tree=None): return {'authority_impact':'unchanged','task_content_impact':'unchanged','integration_impact':'compatible','reviewed_scope':['authority','planning','delta'],'key_delta_refs':['base.txt'],'validation_evidence':['candidate clean'],'unverified_boundaries':[],'summary':'Compatible.','typed_exit':'reconciled','route_payload':({} if candidate_tree is None else {'candidate_tree_sha256':candidate_tree,'relevant_paths':['base.txt']})}
    def continuity_gate(self,candidate_tree):
        gate=self.gate(); gate.update({'integration_impact':'continuity_review_required','typed_exit':'review_continuity_required','route_payload':{'candidate_tree_sha256':candidate_tree,'relevant_paths':['base.txt']},'summary':'Compatible post-review base delta requires a current reviewed-content identity.'}); return gate
    def candidate_tree(self):
        request=self.write('continuity-candidate.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[]})
        return execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)])['candidate_tree_sha256']
    def execute_reconciliation(self,profile):
        candidate_tree=self.candidate_tree(); public=self.public(profile)
        request={'profile':profile,'task_ref':self.task_ref,'delivery_key':self.delivery_key,'branch':'feature','prior_task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'resume_target':public['resume_target'],'candidate_tree_sha256':candidate_tree,'commit_message':'chore(base): reconcile reviewed task'}
        if profile in {'delivery_post_branch_review','delivery_post_publication','delivery_finalizer_base_mismatch'}: request['branch_review_commit']=self.head
        receipt=execute.reconcile(PACKAGE,['--root',str(self.repo),'--request',str(self.write(profile+'-reconciliation-request.json',request))])
        return public,candidate_tree,receipt
    def expose_new_task_files(self):
        (self.repo/'.gitignore').write_text('.trellis/.runtime/\n')
        self.git('add','.gitignore'); self.git('commit','-qm','make task artifacts visible')
        self.head=self.git('rev-parse','HEAD')
        self.assertIn('?? .trellis/',self.git('status','--short'))
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

    def prior_index_digest(self):
        # Independent byte oracle: the original per-entry algorithm, no batch helper.
        staged = subprocess.run(
            ['git', 'ls-files', '--stage', '-z'], cwd=self.repo,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
        ).stdout
        rows = []
        for entry in staged.split(b'\0'):
            if not entry:
                continue
            metadata, path = entry.split(b'\t', 1)
            mode, oid, stage = metadata.split()
            self.assertEqual(b'0', stage)
            if mode == b'160000':
                rows.append(path + b'\0' + mode + b'\0' + oid + b'\0')
            else:
                blob = subprocess.run(
                    ['git', 'cat-file', 'blob', oid.decode('ascii')], cwd=self.repo,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                ).stdout
                rows.append(path + b'\0' + hashlib.sha256(blob).hexdigest().encode() + b'\0')
        return hashlib.sha256(b''.join(rows)).hexdigest()

    def test_batch_digest_matches_old_byte_oracle_with_all_entry_types(self):
        self.add_uninitialized_gitlink()
        files = {'empty': b'', 'binary': bytes(range(256)),
                 '重复\tfile\n.txt': b'shared\0content\n',
                 'duplicate': b'shared\0content\n', 'executable': b'#!/bin/sh\n'}
        for name, content in files.items():
            (self.repo / name).write_bytes(content)
        (self.repo / 'link').symlink_to('missing-target')
        self.git('add', '.')
        self.git('update-index', '--chmod=+x', 'executable')
        expected = self.prior_index_digest()
        self.assertEqual(expected, index_tree_digest(self.repo))
        self.git('update-index', '--chmod=-x', 'executable')
        self.assertEqual(expected, index_tree_digest(self.repo))

    def test_batch_reads_and_hashes_each_unique_blob_once_using_files(self):
        assets = self.repo / 'assets'
        assets.mkdir()
        for number in range(1800):
            (assets / f'unique-{number}').write_bytes(str(number).encode())
        for number in range(100):
            (assets / f'duplicate-{number}').write_bytes(b'shared')
        (assets / 'large').write_bytes(bytes(range(256)) * 8193)
        self.git('add', '.')
        staged = subprocess.run(['git', 'ls-files', '--stage', '-z'], cwd=self.repo,
                                stdout=subprocess.PIPE, check=True).stdout
        expected_oids = list(dict.fromkeys(
            entry.split(b'\t', 1)[0].split()[1]
            for entry in staged.split(b'\0') if entry))
        run = subprocess.run
        requests_seen = []

        def observe(argv, **kwargs):
            if argv[:2] == ['git', 'cat-file']:
                self.assertEqual(['git', 'cat-file', '--batch'], argv)
                for stream in ('stdin', 'stdout'):
                    self.assertTrue(stat.S_ISREG(os.fstat(kwargs[stream].fileno()).st_mode))
                requests_seen.append(kwargs['stdin'].read().splitlines())
                kwargs['stdin'].seek(0)
            return run(argv, **kwargs)

        with mock.patch.object(subprocess, 'run', side_effect=observe), \
                mock.patch.object(common.hashlib, 'sha256', wraps=hashlib.sha256) as hashes:
            actual = index_tree_digest(self.repo)
        self.assertEqual([expected_oids], requests_seen)
        self.assertEqual(len(expected_oids) + 1, hashes.call_count)
        self.assertRegex(actual, r'^[0-9a-f]{64}$')

    def test_batch_missing_blob_keeps_candidate_index_error(self):
        path = self.repo / 'incomplete-object.txt'
        path.write_text('object absent from incomplete local object store\n')
        self.git('add', path.name)
        oid = self.git('rev-parse', ':' + path.name)
        (self.repo / '.git/objects' / oid[:2] / oid[2:]).unlink()
        with self.assertRaises(CommandError) as raised:
            index_tree_digest(self.repo)
        self.assertEqual('candidate_failed', raised.exception.code)
        self.assertEqual('repository.index', raised.exception.field_path)

    def test_committed_memo_follows_actual_tree_and_never_caches_index(self):
        memo = {}
        original = common.committed_tree_digest(self.repo, tree_memo=memo)
        with mock.patch.object(common, 'index_tree_digest', wraps=index_tree_digest) as scans:
            self.assertEqual(original, common.committed_tree_digest(self.repo, tree_memo=memo))
            self.assertEqual(0, scans.call_count)
            (self.repo / 'task.txt').write_text('new index contents\n')
            self.git('add', 'task.txt')
            changed = index_tree_digest(self.repo)
            self.assertNotEqual(original, changed)
            self.assertEqual(original, common.committed_tree_digest(self.repo, tree_memo=memo))
            self.git('commit', '-qm', 'new actual tree')
            self.assertEqual(changed, common.committed_tree_digest(self.repo, tree_memo=memo))
            self.assertEqual(1, scans.call_count)
            # An independent caller receives no previous invocation's memo.
            self.assertEqual(changed, common.committed_tree_digest(self.repo))
            self.assertEqual(2, scans.call_count)

    def test_invoke_scans_once_but_validates_both_results_independently(self):
        public, candidate, receipt = self.execute_reconciliation('delivery_post_check')
        owner = record.run(PACKAGE, {}, [
            '--root', str(self.repo), '--skill-input', str(self.write('memo-public.json', public)),
            '--semantic-review-file', str(self.write('memo-gate.json', self.gate(candidate))),
            '--typed-exit', 'reconciled',
            '--reconciliation-result', str(self.write('memo-receipt.json', receipt)),
        ])
        envelope = self.write('memo-envelope.json', {'public_input': public, 'owner_result': owner})
        checkpoint = common.checkpoint_path(self.repo, self.task_ref, delivery_key=self.delivery_key)
        with mock.patch.object(common, 'index_tree_digest', wraps=index_tree_digest) as scans, \
                mock.patch.object(invoke, 'validate_result', wraps=common.validate_result) as validations, \
                mock.patch.object(common, 'validate_json', wraps=common.validate_json) as schemas, \
                mock.patch.object(common, 'objective_identity', wraps=common.objective_identity) as identities, \
                mock.patch.object(common, 'is_ancestor', wraps=common.is_ancestor) as ancestors, \
                mock.patch.object(common, 'committed_tree_digest', wraps=common.committed_tree_digest) as comparisons:
            output = invoke.run(PACKAGE, {}, ['--root', str(self.repo), '--invocation', str(envelope)])
        self.assertEqual('reconciled', output['exit_id'])
        self.assertFalse(checkpoint.exists())
        self.assertEqual(1, scans.call_count)
        self.assertEqual(2, validations.call_count)
        self.assertIsNot(validations.call_args_list[0].args[2], validations.call_args_list[1].args[2])
        self.assertEqual(2, sum(call.args[2] == 'owner_result' for call in schemas.call_args_list))
        self.assertEqual(2, identities.call_count)
        self.assertEqual(4, ancestors.call_count)
        self.assertEqual(2, comparisons.call_count)

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
            with mock.patch.object(execute, 'index_tree_digest', side_effect=observe_index), mock.patch.object(execute, 'committed_tree_digest', wraps=execute.committed_tree_digest) as committed_digest:
                public, candidate_tree, receipt = self.execute_reconciliation('delivery_post_branch_review')
            reconciled = receipt['reconciled_task_head']
            self.assertEqual(2, len(observations))
            self.assertEqual([candidate_tree] * 2, [row[2] for row in observations])
            self.assertEqual([self.new, self.head], [row[1] for row in observations])
            self.assertEqual(self.repo.resolve(), observations[1][0].resolve())
            committed_digest.assert_called_once()
            self.assertEqual(self.repo.resolve(),committed_digest.call_args.args[0].resolve())
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
    def test_delivery_review_pair_resumes_delivery_publication(self):
        public=self.public('delivery_post_publication')
        public,candidate_tree,receipt=self.execute_reconciliation('delivery_post_publication')
        owner=record.run(PACKAGE,{},[
            '--root',str(self.repo),'--skill-input',str(self.write('delivery-public.json',public)),
            '--semantic-review-file',str(self.write('delivery-gate.json',self.continuity_gate(candidate_tree))),
            '--typed-exit','review_continuity_required',
            '--reconciliation-result',str(self.write('delivery-receipt.json',receipt)),
        ])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('delivery-envelope.json',{'public_input':public,'owner_result':owner}))])
        self.assertEqual(('review_continuity_required','delivery_publication'),(output['exit_id'],output['resume_target']))
    def test_pre_review_input_rejects_caller_supplied_pair(self):
        public=self.public('delivery_post_commit'); public.update({'old_base_head':self.old,'new_base_head':self.new})
        with self.assertRaises(CommandError) as raised:
            common.validate_public(PACKAGE,public)
        self.assertEqual('schema_mismatch',raised.exception.code)
    def test_post_plan_accepts_planning_before_activation_but_later_boundaries_do_not(self):
        self.write_identity(status='planning')
        self.assertNotIn('branch', json.loads((self.task_dir/'task.json').read_text()))
        self.assertFalse((self.repo/'.trellis/.runtime/guru-team/tasks').exists())
        self.assertFalse((self.repo/'.trellis/.runtime/guru-team/workspaces').exists())
        public,candidate_tree,receipt=self.execute_reconciliation('delivery_post_plan'); post_plan=public
        public_path=self.write('planning-new-pair.json',post_plan); gate_path=self.write('planning-gate.json',self.gate(candidate_tree)); receipt_path=self.write('planning-receipt.json',receipt)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled','--reconciliation-result',str(receipt_path)])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('planning-envelope.json',{'public_input':post_plan,'owner_result':owner}))])
        self.assertEqual('delivery_activation',output['resume_target'])
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled','--reconciliation-result',str(receipt_path)])
        recovered=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('planning-recovery.json',{'public_input':post_plan,'owner_result':owner}))])
        self.assertEqual(output,recovered)
    def test_new_planning_task_survives_pre_review_base_reconciliation(self):
        self.expose_new_task_files()
        self.write_identity(status='planning')
        original=(self.task_dir/'task.json').read_bytes()
        public,candidate_tree,receipt=self.execute_reconciliation('delivery_post_plan')
        self.assertEqual(original,(self.task_dir/'task.json').read_bytes())
        self.assertIn('?? .trellis/',self.git('status','--short'))
        self.assertEqual('',self.git('stash','list'))
        path=self.write('dirty-plan-public.json',public)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(path),'--semantic-review-file',str(self.write('dirty-plan-gate.json',self.gate(candidate_tree))),'--typed-exit','reconciled','--reconciliation-result',str(self.write('dirty-plan-receipt.json',receipt))])
        self.assertEqual('reconciled',owner['typed_output']['exit_id'])
    def test_staged_and_unstaged_implementation_survives_pre_review_reconciliation(self):
        self.expose_new_task_files()
        (self.repo/'task.txt').write_text('staged\n'); self.git('add','task.txt')
        (self.repo/'task.txt').write_text('unstaged\n')
        staged=self.git('show',':task.txt'); worktree=(self.repo/'task.txt').read_bytes()
        public,candidate_tree,receipt=self.execute_reconciliation('delivery_post_check')
        self.assertEqual(staged,self.git('show',':task.txt'))
        self.assertEqual(worktree,(self.repo/'task.txt').read_bytes())
        self.assertIn('MM task.txt',self.git('status','--short'))
        self.assertEqual('',self.git('stash','list'))
        path=self.write('dirty-check-public.json',public)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(path),'--semantic-review-file',str(self.write('dirty-check-gate.json',self.gate(candidate_tree))),'--typed-exit','reconciled','--reconciliation-result',str(self.write('dirty-check-receipt.json',receipt))])
        self.assertEqual('reconciled',owner['typed_output']['exit_id'])
    def test_dirty_candidate_mismatch_aborts_and_restores_planning(self):
        self.expose_new_task_files(); self.write_identity(status='planning')
        before=self.git('status','--porcelain=v1'); task=(self.task_dir/'task.json').read_bytes()
        request={'profile':'delivery_post_plan','task_ref':self.task_ref,'delivery_key':self.delivery_key,'branch':'feature','prior_task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'resume_target':'delivery_activation','candidate_tree_sha256':'0'*64,'commit_message':'chore(base): reconcile reviewed task'}
        with self.assertRaises(CommandError) as raised:
            execute.reconcile(PACKAGE,['--root',str(self.repo),'--request',str(self.write('dirty-mismatch.json',request))])
        self.assertEqual('stale_identity',raised.exception.code)
        self.assertEqual(self.head,self.git('rev-parse','HEAD'))
        self.assertEqual(before,self.git('status','--porcelain=v1'))
        self.assertEqual(task,(self.task_dir/'task.json').read_bytes())
        self.assertEqual('',self.git('stash','list'))
    def test_preexisting_stash_is_preserved_after_dirty_reconciliation(self):
        (self.repo/'base.txt').write_text('existing pending work\n')
        self.git('stash','push','-m','existing stash')
        previous=self.git('rev-parse','refs/stash')
        self.expose_new_task_files(); self.write_identity(status='planning')
        self.execute_reconciliation('delivery_post_plan')
        self.assertEqual(previous,self.git('rev-parse','refs/stash'))
        self.assertIn('?? .trellis/',self.git('status','--short'))
    def test_dirty_submodule_stop_restores_shelved_task_changes(self):
        self.add_uninitialized_gitlink()
        subprocess.run(['git','-c','protocol.file.allow=always','submodule','update','--init','vendor/child'],cwd=self.repo,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (self.repo/'task.txt').write_text('pending task work\n')
        child=self.repo/'vendor/child/child.txt'; child.write_text('pending child work\n')
        before=self.git('status','--short')
        request={'profile':'delivery_post_check','task_ref':self.task_ref,'delivery_key':self.delivery_key,'branch':'feature','prior_task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'resume_target':'task_commit','candidate_tree_sha256':'0'*64,'commit_message':'chore(base): reconcile reviewed task'}
        with self.assertRaises(CommandError) as raised:
            execute.reconcile(PACKAGE,['--root',str(self.repo),'--request',str(self.write('dirty-submodule.json',request))])
        self.assertEqual('stale_identity',raised.exception.code)
        self.assertEqual('worktree',raised.exception.field_path)
        self.assertEqual(self.head,self.git('rev-parse','HEAD'))
        self.assertEqual(before,self.git('status','--short'))
        self.assertEqual('pending task work\n',(self.repo/'task.txt').read_text())
        self.assertEqual('pending child work\n',child.read_text())
        self.assertEqual('',self.git('stash','list'))
    def test_post_review_dirty_worktree_stops_without_shelving(self):
        (self.repo/'task.txt').write_text('pending post-review work\n')
        before=self.git('status','--short')
        request={'profile':'delivery_post_branch_review','task_ref':self.task_ref,'delivery_key':self.delivery_key,'branch':'feature','prior_task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'resume_target':'publication_review','branch_review_commit':self.head,'candidate_tree_sha256':'0'*64,'commit_message':'chore(base): reconcile reviewed task'}
        with self.assertRaises(CommandError) as raised:
            execute.reconcile(PACKAGE,['--root',str(self.repo),'--request',str(self.write('dirty-post-review.json',request))])
        self.assertEqual('stale_identity',raised.exception.code)
        self.assertEqual('worktree',raised.exception.field_path)
        self.assertEqual(before,self.git('status','--short'))
        self.assertEqual('',self.git('stash','list'))
    def test_unrelated_post_plan_base_delta_preserves_task_activation(self):
        self.write_identity(status='planning')
        public,candidate_tree,receipt=self.execute_reconciliation('delivery_post_plan'); public_path=self.write('unrelated-post-plan.json',public)
        gate=self.gate(candidate_tree); gate.update({'key_delta_refs':['unrelated-base-only.txt'],'validation_evidence':['base-only delta is unrelated and candidate validations passed'],'summary':'Only the integration clock advanced; authority and approved planning assumptions remain current.'})
        gate_path=self.write('unrelated-post-plan-gate.json',gate)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled','--reconciliation-result',str(self.write('unrelated-post-plan-receipt.json',receipt))])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('unrelated-post-plan-envelope.json',{'public_input':public,'owner_result':owner}))])
        self.assertEqual('reconciled',output['exit_id'])
        self.assertEqual('delivery_activation',output['resume_target'])
    def test_real_planning_authority_change_remains_planning_stale(self):
        self.write_identity(status='planning')
        public=self.public('delivery_post_plan'); public_path=self.write('authority-change-post-plan.json',public)
        gate=self.gate(); gate.update({'authority_impact':'changed','task_content_impact':'planning_stale','integration_impact':'compatible','summary':'Live Issue authority invalidated an approved planning assumption.','typed_exit':'planning_stale','route_payload':{'reason_refs':['live-issue-authority-changed']}})
        gate_path=self.write('authority-change-post-plan-gate.json',gate)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(public_path),'--semantic-review-file',str(gate_path),'--typed-exit','planning_stale'])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('authority-change-post-plan-envelope.json',{'public_input':public,'owner_result':owner}))])
        self.assertEqual({'exit_id':'planning_stale','task_ref':self.task_ref,'delivery_key':self.delivery_key,'reason_refs':['live-issue-authority-changed']},output)
    def test_multiple_base_commits_form_one_cumulative_pair(self):
        self.git('switch','main'); (self.repo/'second.txt').write_text('second\n'); self.git('add','second.txt'); self.git('commit','-qm','second base advance'); newest=self.git('rev-parse','HEAD'); self.git('switch','feature')
        public=self.public(); public['selected_base_ref']=newest
        self.assertEqual((self.head,self.old,newest),common.operation_pair(self.repo,public))
    def test_candidate_is_clean_and_leaves_no_worktree(self):
        request=self.write('request.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[['git','status','--short']]}); result=execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)]); self.assertEqual('clean',result['merge_status']); self.assertRegex(result['candidate_tree_sha256'],r'^[0-9a-f]{64}$'); self.assertEqual([],result['conflict_paths']); self.assertNotIn('guru-base-candidate-',self.git('worktree','list'))
    def test_candidate_routes_python_validation_through_managed_interpreter(self):
        request=self.write('python-request.json',{'task_head':self.head,'new_base_head':self.new,'validation_commands':[['python3','-c','import sys; raise SystemExit(0 if sys.executable else 1)']]}); result=execute.candidate(PACKAGE,['--root',str(self.repo),'--request',str(request)]); self.assertEqual(sys.executable,result['validations'][0]['argv'][0]); self.assertEqual(0,result['validations'][0]['exit_code'])
    def test_post_review_profiles_create_one_local_commit_and_publish_current_head(self):
        for profile in ('delivery_post_branch_review','delivery_post_publication','delivery_finalizer_base_mismatch'):
            with self.subTest(profile=profile):
                public,candidate_tree,receipt=self.execute_reconciliation(profile)
                reconciled=receipt['reconciled_task_head']; self.assertEqual([self.head,self.new],self.git('show','-s','--format=%P',reconciled).split()); self.assertEqual('',self.git('status','--short'))
                gate=self.continuity_gate(candidate_tree); owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(self.write(profile+'-public.json',public)),'--semantic-review-file',str(self.write(profile+'-gate.json',gate)),'--typed-exit','review_continuity_required','--reconciliation-result',str(self.write(profile+'-receipt.json',receipt))])
                output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write(profile+'-envelope.json',{'public_input':public,'owner_result':owner}))])
                self.assertEqual('review_continuity_required',output['exit_id']); self.assertEqual(reconciled,output['task_head']); self.assertEqual(self.head,output['branch_review_commit']); self.assertEqual(candidate_tree,output['candidate_tree_sha256'])
                self.git('reset','--hard',self.head)
    def test_pre_review_compatible_reconciliation_commits_and_reenters_phase2(self):
        for profile in ('delivery_post_check','delivery_post_commit'):
            with self.subTest(profile=profile):
                public,candidate_tree,receipt=self.execute_reconciliation(profile)
                reconciled=receipt['reconciled_task_head']
                self.assertEqual([self.head,self.new],self.git('show','-s','--format=%P',reconciled).split())
                self.assertNotIn('branch_review_commit',receipt)
                owner=record.run(PACKAGE,{},[
                    '--root',str(self.repo),'--skill-input',str(self.write(profile+'-pre-public.json',public)),
                    '--semantic-review-file',str(self.write(profile+'-pre-gate.json',self.gate(candidate_tree))),
                    '--typed-exit','reconciled','--reconciliation-result',str(self.write(profile+'-pre-receipt.json',receipt)),
                ])
                output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write(profile+'-pre-envelope.json',{'public_input':public,'owner_result':owner}))])
                self.assertEqual('phase2',output['resume_target'])
                self.assertEqual(reconciled,output['task_head'])
                self.git('reset','--hard',self.head)
    def test_post_commit_cannot_enter_base_continuity(self):
        public,candidate_tree,receipt=self.execute_reconciliation('delivery_post_commit')
        with self.assertRaises(CommandError) as raised:
            record.run(PACKAGE,{},[
                '--root',str(self.repo),'--skill-input',str(self.write('post-commit-continuity-public.json',public)),
                '--semantic-review-file',str(self.write('post-commit-continuity-gate.json',self.continuity_gate(candidate_tree))),
                '--typed-exit','review_continuity_required','--reconciliation-result',str(self.write('post-commit-continuity-receipt.json',receipt)),
            ])
        self.assertEqual('schema_mismatch',raised.exception.code)
    def test_post_review_current_pair_recovers_after_reconciliation_commit(self):
        public,candidate_tree,receipt=self.execute_reconciliation('delivery_finalizer_base_mismatch')
        gate=self.continuity_gate(candidate_tree)
        owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(self.write('recovery-public.json',public)),'--semantic-review-file',str(self.write('recovery-gate.json',gate)),'--typed-exit','review_continuity_required','--reconciliation-result',str(self.write('recovery-receipt.json',receipt))])
        output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(self.write('recovery-envelope.json',{'public_input':public,'owner_result':owner}))])
        self.assertEqual(owner['typed_output'],output)
        self.assertEqual(receipt['reconciled_task_head'],output['task_head'])
    def resolved_merge(self,public_check=False):
        (self.repo/'conflict.txt').write_text('task\n'); self.git('add','conflict.txt'); self.git('commit','-qm','task conflict'); phase2=self.git('rev-parse','HEAD')
        if public_check:
            projection=DeliveryProjection(self.repo,self.task_ref)
            plan=projection.planning_directory(self.delivery_key)/'design.md'; plan.write_text('本 Delivery 当前计划\n')
            projection.apply({'api_version':'1.0','operation':'record_gate','key':self.delivery_key,
                              'owner_role':'planning','owner_id':DECLARATION['owners']['planning'],'expected_phase':'planning',
                              'result':{'result_id':'planning-resolved-fixture','owner_role':'planning',
                                        'owner_id':DECLARATION['owners']['planning'],'outcome':'accepted',
                                        'scope_ref':projection.resolve(self.delivery_key)['scope_ref'],
                                        'plan_ref':authority_ref(plan,self.repo),'candidate':None,'predecessor_result_id':None,
                                        'obligations':[],'evidence':[authority_ref(plan,self.repo)]}})
            projection.begin_check(self.delivery_key,projection.candidate(['base.txt','task.txt','conflict.txt'],head_ref=phase2,base_ref=self.new))
            record_gate(projection,self.delivery_key,'check','check-before-reconciliation','passed',[authority_ref(plan,self.repo)],[])
        self.git('switch','main'); (self.repo/'conflict.txt').write_text('base\n'); self.git('add','conflict.txt'); self.git('commit','-qm','base conflict'); new=self.git('rev-parse','HEAD'); self.git('switch','feature')
        merge=subprocess.run(['git','merge','--no-commit','--no-ff',new],cwd=self.repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.assertNotEqual(0,merge.returncode); (self.repo/'conflict.txt').write_text('resolved\n'); self.git('add','conflict.txt')
        tree=self.git('write-tree'); digest=index_tree_digest(self.repo)
        request={'profile':'delivery_resolved_candidate','mode':'workflow','source_exit':'resolved_reconciliation_passed','task_ref':self.task_ref,'delivery_key':self.delivery_key,'phase2_commit_anchor':phase2,'branch':'feature','selected_base_ref':new,'old_base_head':self.new,'new_base_head':new,'merge_head':new,'stage0_tree':tree,'index_tree_sha256':digest,'parent_order':[phase2,new],'commit_message':'chore(base): record resolved reconciliation','resume_target':'branch_review'}
        return request

    def fresh_resolved_check(self,request):
        projection=DeliveryProjection(self.repo,self.task_ref)
        reason=authority_ref(projection.planning_directory(self.delivery_key)/'design.md',self.repo)
        rework(projection,self.delivery_key,'full_review','implementation',reason,['check','full_review','readiness'])
        candidate=projection.candidate(['base.txt','task.txt','conflict.txt'],head_ref=self.git('rev-parse','HEAD'),base_ref=self.new)
        projection.begin_check(self.delivery_key,candidate)
        record_gate(projection,self.delivery_key,'check','check-after-reconciliation','passed',[reason],[])

    def project_resolved(self,request,result,check_id):
        import project
        authoring={'profile':'delivery_branch_review','mode':'workflow','base_ref':self.new,
                   'review_intent':'initial_review','check_result_id':check_id}
        return project.run(PACKAGE,{'id':'project-resolved-full-review'},[
            '--root',str(self.repo),'--input',str(self.write('project-resolved-input.json',request)),
            '--result',str(self.write('project-resolved-result.json',result)),
            '--authoring',str(self.write('project-resolved-authoring.json',authoring))])

    def test_resolved_candidate_commits_once_and_recovers_same_commit(self):
        request=self.resolved_merge(public_check=True); path=self.write('resolved-input.json',request)
        first=execute.resolved_reconcile(PACKAGE,['--root',str(self.repo),'--input',str(path)])
        self.assertEqual('committed',first['status']); commit=first['reconciled_task_head']
        self.assertEqual(request['parent_order'],self.git('show','-s','--format=%P',commit).split())
        second=execute.resolved_reconcile(PACKAGE,['--root',str(self.repo),'--input',str(path)])
        self.assertEqual('recovered',second['status']); self.assertEqual(commit,second['reconciled_task_head'])
        with self.assertRaises(CommandError) as raised:
            self.project_resolved(request,second,'check-before-reconciliation')
        self.assertEqual('stale_identity',raised.exception.code)
        self.fresh_resolved_check(request)
        output=self.project_resolved(request,second,'check-after-reconciliation')
        self.assertEqual({'profile':'delivery_branch_review','mode':'workflow','task_ref':self.task_ref,'delivery_key':self.delivery_key,'base_ref':self.new,'branch_review_commit':commit,'review_intent':'initial_review','check_result_id':'check-after-reconciliation'},output)
        self.assertEqual(output,self.project_resolved(request,second,'check-after-reconciliation'))
        self.assertEqual(commit,self.git('rev-parse','HEAD'))

    def resolved_projection_after_normal_edit(self,changed):
        request=self.resolved_merge(public_check=True)
        result=execute.resolved_reconcile(PACKAGE,['--root',str(self.repo),'--input',str(self.write('live-input.json',request))])
        self.fresh_resolved_check(request)
        projection=DeliveryProjection(self.repo,self.task_ref)
        path=self.repo/'conflict.txt' if changed=='candidate' else projection.planning_directory(self.delivery_key)/'design.md'
        path.write_text(path.read_text()+'正常下一轮修改\n')
        with self.assertRaises(CommandError) as raised:
            self.project_resolved(request,result,'check-after-reconciliation')
        self.assertEqual('stale_identity',raised.exception.code)

    def test_resolved_projection_requires_live_candidate(self):
        self.resolved_projection_after_normal_edit('candidate')

    def test_resolved_projection_requires_current_plan(self):
        self.resolved_projection_after_normal_edit('plan')

    def test_resolved_candidate_accepts_task_head_tree_after_conflict_resolution(self):
        (self.repo/'base.txt').write_text('new\n')
        (self.repo/'conflict.txt').write_text('task\n')
        self.git('add','base.txt','conflict.txt'); self.git('commit','-qm','task conflict')
        phase2=self.git('rev-parse','HEAD')
        self.git('switch','main')
        (self.repo/'conflict.txt').write_text('base\n')
        self.git('add','conflict.txt'); self.git('commit','-qm','base conflict')
        new=self.git('rev-parse','HEAD')
        self.git('switch','feature')
        merge=subprocess.run(['git','merge','--no-commit','--no-ff',new],cwd=self.repo,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.assertNotEqual(0,merge.returncode)
        self.git('checkout','--ours','--','conflict.txt'); self.git('add','conflict.txt')
        tree=self.git('write-tree'); digest=index_tree_digest(self.repo)
        self.assertEqual(self.git('show','-s','--format=%T',phase2),tree)
        self.assertEqual('',self.git('diff','--cached'))
        request={'profile':'delivery_resolved_candidate','mode':'workflow','source_exit':'resolved_reconciliation_passed','task_ref':self.task_ref,'delivery_key':self.delivery_key,'phase2_commit_anchor':phase2,'branch':'feature','selected_base_ref':new,'old_base_head':self.new,'new_base_head':new,'merge_head':new,'stage0_tree':tree,'index_tree_sha256':digest,'parent_order':[phase2,new],'commit_message':'chore(base): record resolved reconciliation','resume_target':'branch_review'}
        path=self.write('task-head-tree-resolved-input.json',request)

        first=execute.resolved_reconcile(PACKAGE,['--root',str(self.repo),'--input',str(path)])
        commit=first['reconciled_task_head']
        self.assertEqual('committed',first['status'])
        self.assertEqual([phase2,new],self.git('show','-s','--format=%P',commit).split())
        self.assertEqual(tree,self.git('show','-s','--format=%T',commit))
        self.assertEqual('',self.git('status','--short'))

        second=execute.resolved_reconcile(PACKAGE,['--root',str(self.repo),'--input',str(path)])
        self.assertEqual('recovered',second['status'])
        self.assertEqual(commit,second['reconciled_task_head'])

    def test_resolved_candidate_rejects_unresolved_unstaged_untracked_and_other_sequencer(self):
        cases=('unresolved','unstaged','untracked','sequencer')
        for case in cases:
            with self.subTest(case=case):
                if case!='unresolved':
                    request=self.resolved_merge()
                else:
                    request=self.resolved_merge(); self.git('reset','conflict.txt')
                if case=='unstaged': (self.repo/'conflict.txt').write_text('unstaged\n')
                if case=='untracked': (self.repo/'extra.txt').write_text('extra\n')
                if case=='sequencer':
                    path=Path(self.git('rev-parse','--git-path','sequencer')); path=path if path.is_absolute() else self.repo/path; path.mkdir(parents=True)
                with self.assertRaises(CommandError): execute.resolved_reconcile(PACKAGE,['--root',str(self.repo),'--input',str(self.write(case+'-resolved.json',request))])
                self.tmp.cleanup(); self.setUp()
    def test_reconciliation_stale_dirty_and_candidate_mismatch_fail_without_commit(self):
        candidate_tree=self.candidate_tree(); base={'profile':'delivery_post_branch_review','task_ref':self.task_ref,'delivery_key':self.delivery_key,'branch':'feature','prior_task_head':self.head,'selected_base_ref':self.new,'old_base_head':self.old,'new_base_head':self.new,'resume_target':'publication_review','branch_review_commit':self.head,'candidate_tree_sha256':candidate_tree,'commit_message':'chore(base): reconcile reviewed task'}
        cases=[('stale-head',{**base,'prior_task_head':self.old},None),('candidate',{**base,'candidate_tree_sha256':'f'*64},None),('dirty',base,lambda:(self.repo/'dirty.txt').write_text('dirty\n'))]
        for name,request,mutate in cases:
            with self.subTest(name=name):
                if mutate: mutate()
                with self.assertRaises(CommandError): execute.reconcile(PACKAGE,['--root',str(self.repo),'--request',str(self.write(name+'-request.json',request))])
                self.assertEqual(self.head,self.git('rev-parse','HEAD'))
                if name=='dirty': (self.repo/'dirty.txt').unlink()
                self.assertNotEqual(0,subprocess.run(['git','rev-parse','--verify','--quiet','MERGE_HEAD'],cwd=self.repo,stdout=subprocess.PIPE,stderr=subprocess.PIPE).returncode)
    def test_record_invoke_consumes_checkpoint_once(self):
        public=self.public('delivery_finalizer_base_mismatch'); pi=self.write('public.json',public); gate=self.write('gate.json',self.gate()); result=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gate),'--typed-exit','reconciled']); envelope=self.write('envelope.json',{'public_input':public,'owner_result':result}); output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)]); self.assertEqual('reconciled',output['exit_id']); checkpoint=self.repo/'.trellis/.runtime/guru-team/owner-checkpoints/current/guru-reconcile-task-base/base-reconciliation.json'; self.assertFalse(checkpoint.exists())
        with self.assertRaises(CommandError) as raised:
            invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])
        self.assertEqual('stale_identity',raised.exception.code)
    def test_reconciled_requires_complete_compatible_evidence(self):
        public=self.public('delivery_finalizer_base_mismatch'); pi=self.write('reconciled-public.json',public)
        mutations=(('authority_impact','insufficient_evidence'),('task_content_impact','insufficient_evidence'),('integration_impact','insufficient_evidence'),('unverified_boundaries',['live validation unavailable']))
        for field,value in mutations:
            with self.subTest(field=field):
                gate=self.gate(); gate[field]=value; gate_path=self.write('invalid-'+field+'.json',gate)
                with self.assertRaises(CommandError) as raised:
                    record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gate_path),'--typed-exit','reconciled'])
                self.assertEqual('schema_mismatch',raised.exception.code)
    def test_current_pair_preserves_each_semantic_exit_and_retires_once(self):
        cases={
            'reconciled':('delivery_finalizer_base_mismatch',{}),
            'implementation_required':('delivery_finalizer_base_mismatch',{'finding_refs':['finding-1']}),
            'planning_stale':('delivery_finalizer_base_mismatch',{'reason_refs':['planning-1']}),
            'scope_confirmation_required':('delivery_finalizer_base_mismatch',{'proposal_refs':['proposal-1']}),
            'blocked':('delivery_finalizer_base_mismatch',{}),
        }
        for exit_id,(profile,payload) in cases.items():
            with self.subTest(exit_id=exit_id):
                public=self.public(profile); pi=self.write(exit_id+'-public.json',public); gate=self.gate(); gate.update({'typed_exit':exit_id,'route_payload':payload}); gp=self.write(exit_id+'-gate.json',gate)
                owner=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gp),'--typed-exit',exit_id])
                envelope=self.write(exit_id+'-envelope.json',{'public_input':public,'owner_result':owner})
                output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])
                self.assertEqual(owner['typed_output'],output)
                with self.assertRaises(CommandError):
                    invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])
    def test_132_161_replay_preserves_review_head_and_resumes_finalizer(self):
        public=self.public('delivery_finalizer_base_mismatch'); pi=self.write('historical-finalizer.json',public); gate=self.gate(); gate['reviewed_scope'].append('historical #132/#161 base-only stale route'); gp=self.write('historical-gate.json',gate)
        result=record.run(PACKAGE,{},['--root',str(self.repo),'--skill-input',str(pi),'--semantic-review-file',str(gp),'--typed-exit','reconciled']); envelope=self.write('historical-envelope.json',{'public_input':public,'owner_result':result}); output=invoke.run(PACKAGE,{},['--root',str(self.repo),'--invocation',str(envelope)])
        self.assertEqual('finalization_resume',output['resume_target']); self.assertEqual(self.head,public['branch_review_commit']); self.assertNotIn('branch_review_commit',output)
    def test_history_rewrite_blocks(self):
        public=self.public('delivery_post_branch_review'); public['old_base_head']=self.head; path=self.write('bad.json',public)
        with self.assertRaises(CommandError) as raised:
            common.objective_identity(self.repo,public)
        self.assertEqual('stale_identity',raised.exception.code)
    def test_task_identity_rejects_typo_status_binding_and_not_current(self):
        cases=[]
        typo=self.public(); typo['task_ref']='.trellis/tasks/typo'; cases.append(('typo',typo,lambda:None))
        stale=self.public(); cases.append(('status',stale,lambda:self.write_identity(status='done')))
        wrong_branch=self.public(); cases.append(('branch',wrong_branch,lambda:self.write_identity(branch='other')))
        missing_binding=self.public(); cases.append(('binding',missing_binding,lambda:BranchBindingStore(inspect_repository(self.repo)).path_for(TaskLifecycleKey(self.task_id,0)).unlink()))
        other_ref='.trellis/tasks/other'; self.write_identity(task_ref=other_ref,task_id='other-task',branch='other'); not_current=self.public(); not_current['task_ref']=other_ref; cases.append(('not-current',not_current,lambda:None))
        for name,public,mutate in cases:
            with self.subTest(name=name):
                self.write_identity(); mutate(); path=self.write('identity-'+name+'.json',public)
                with self.assertRaises(CommandError) as raised:
                    common.objective_identity(self.repo,public)
                self.assertEqual('stale_identity',raised.exception.code)
    def test_reactivated_generation_requires_its_own_branch_binding(self):
        metadata=json.loads((self.task_dir/'task.json').read_text()); metadata['lifecycle_generation']=1
        (self.task_dir/'task.json').write_text(json.dumps(metadata))
        public=self.public('delivery_post_check'); public['selected_base_ref']=self.old
        path=self.write('reactivated-pair.json',public)
        with self.assertRaises(CommandError) as raised:
            common.objective_identity(self.repo,public)
        self.assertEqual('stale_identity',raised.exception.code)
        self.assertEqual('branch_binding',raised.exception.field_path)
        store=BranchBindingStore(inspect_repository(self.repo))
        store.path_for(TaskLifecycleKey(self.task_id,0)).unlink()
        store.establish(TaskLifecycleKey(self.task_id,1),'feature')
        projection=DeliveryProjection(self.repo,self.task_ref)
        scope=projection.read_record()['accepted_scope']
        self.delivery_key={'task_id':self.task_id,'lifecycle_generation':1,'delivery_id':'2b3dc8b6-ec4b-45c0-942b-e642d0770c84'}
        projection.apply({'api_version':'1.0','operation':'create_delivery','key':self.delivery_key,
                          'owner_role':'creation','owner_id':'guru-create-delivery','profile':'pull_request',
                          'scope_ref':{'authority':scope,'anchors':['后续工作']}})
        public['delivery_key']=self.delivery_key; path=self.write('new-generation-pair.json',public)
        self.assertEqual((self.head,self.old,self.old),common.objective_identity(self.repo,public))
    def test_checkpoint_namespace_binds_task_id_and_full_ref(self):
        from common import checkpoint_path
        first=checkpoint_path(self.repo,self.task_ref,delivery_key=self.delivery_key)
        moved='.trellis/tasks/moved-current'
        self.task_dir.rename(self.repo/moved)
        second=checkpoint_path(self.repo,moved,delivery_key=self.delivery_key)
        self.assertEqual(first.parent.parent.name,second.parent.parent.name)
        self.assertIn(self.task_id,first.parent.parent.name)
        self.assertIn(self.task_id,second.parent.parent.name)

    def preimplementation_candidate(self, *, pending=True):
        resolved = self.resolved_merge()
        self.head = resolved['phase2_commit_anchor']
        self.new = resolved['new_base_head']
        tree = resolved['stage0_tree']
        if pending:
            (self.repo / 'task.txt').write_text('pending staged plan\n')
            self.git('add', 'task.txt')
            (self.repo / 'task.txt').write_text('pending unstaged plan\n')
            (self.repo / 'notes.txt').write_text('pending untracked notes\n')
        request = {'profile': 'delivery_post_plan', 'task_ref': self.task_ref,
                   'delivery_key': self.delivery_key, 'branch': 'feature',
                   'prior_task_head': self.head, 'selected_base_ref': self.new,
                   'old_base_head': self.old, 'new_base_head': self.new,
                   'resume_target': 'delivery_activation',
                   'candidate_tree_sha256': resolved['index_tree_sha256'],
                   'commit_message': 'chore(base): reconcile approved planning baseline',
                   'resolved_candidate': {'stage0_tree': tree,
                                          'integration_paths': ['base.txt', 'conflict.txt']}}
        return request

    def preserved_pending_state(self):
        return ((self.repo / '.git/index').read_bytes(),
                self.git('show', ':task.txt'),
                (self.repo / 'task.txt').read_bytes(),
                (self.repo / 'notes.txt').read_bytes(),
                self.git('stash', 'list'))

    def test_post_plan_resolved_preview_commit_and_recovery_preserve_pending(self):
        request = self.preimplementation_candidate()
        before = self.preserved_pending_state()
        marker = self.inputs / 'resolved-validation.json'
        command = [sys.executable, '-c',
                   'import json; from pathlib import Path; import sys; '
                   'Path(sys.argv[1]).write_text(json.dumps({p:Path(p).read_text() '
                   'for p in ("base.txt","conflict.txt","task.txt")}))', str(marker)]
        preview = {'task_head': self.head, 'new_base_head': self.new,
                   'resolved_candidate': request['resolved_candidate'],
                   'validation_commands': [command]}
        result = execute.candidate(PACKAGE, ['--root', str(self.repo), '--request',
                                            str(self.write('resolved-preview.json', preview))])
        self.assertEqual('clean', result['merge_status'])
        self.assertEqual(request['candidate_tree_sha256'], result['candidate_tree_sha256'])
        self.assertEqual([{'argv': command, 'exit_code': 0}], result['validations'])
        self.assertEqual({'base.txt': 'new\n', 'conflict.txt': 'resolved\n', 'task.txt': 'task\n'},
                         json.loads(marker.read_text()))
        self.assertEqual(before, self.preserved_pending_state())
        self.assertEqual(self.new, self.git('rev-parse', 'MERGE_HEAD'))
        self.assertNotIn('guru-base-candidate-', self.git('worktree', 'list'))
        path = self.write('post-plan-resolved-request.json', request)
        first = execute.reconcile(PACKAGE, ['--root', str(self.repo), '--request', str(path)])
        commit = first['reconciled_task_head']
        self.assertEqual([self.head, self.new], self.git('show', '-s', '--format=%P', commit).split())
        self.assertEqual(request['resolved_candidate']['stage0_tree'], self.git('rev-parse', 'HEAD^{tree}'))
        self.assertEqual('task', self.git('show', 'HEAD:task.txt'))
        self.assertFalse((self.repo / '.git/MERGE_HEAD').exists())
        self.assertEqual(before, self.preserved_pending_state())
        count = self.git('rev-list', '--count', 'HEAD')
        second = execute.reconcile(PACKAGE, ['--root', str(self.repo), '--request', str(path)])
        self.assertEqual(first, second)
        self.assertEqual(count, self.git('rev-list', '--count', 'HEAD'))
        self.assertEqual(before, self.preserved_pending_state())

    def test_fixed_resolved_target_completes_after_branch_advance(self):
        request = self.preimplementation_candidate()
        fixed = request['new_base_head']
        # A real independent commit advances the target ref during resolution.
        tree = self.git('rev-parse', fixed + '^{tree}')
        process = subprocess.run(['git', 'commit-tree', tree, '-p', fixed, '-m', 'independent target advancement'], cwd=self.repo, text=True, capture_output=True, check=True)
        advanced = process.stdout.strip()
        self.git('update-ref', 'refs/heads/main', advanced)
        receipt = execute.reconcile(PACKAGE, ['--root', str(self.repo), '--request', str(self.write('fixed-target.json', request))])
        self.assertEqual([request['prior_task_head'], fixed], self.git('show', '-s', '--format=%P', receipt['reconciled_task_head']).split())
        self.assertEqual(advanced, self.git('rev-parse', 'main'))
        self.assertEqual(receipt, execute.reconcile(PACKAGE, ['--root', str(self.repo), '--request', str(self.write('fixed-target-recovery.json', request))]))

    def test_post_plan_resolved_normal_changes_stop_and_preserve_state(self):
        for case in ('unresolved', 'unstaged', 'index', 'mode', 'candidate_paths',
                     'candidate_digest', 'head', 'sequencer'):
            with self.subTest(case=case):
                request = self.preimplementation_candidate()
                if case == 'unresolved':
                    self.git('checkout', '-m', '--', 'conflict.txt')
                    self.assertTrue(self.git('ls-files', '--unmerged'))
                elif case == 'unstaged':
                    (self.repo / 'conflict.txt').write_text('next unstaged resolution\n')
                elif case == 'index':
                    (self.repo / 'conflict.txt').write_text('next staged resolution\n')
                    self.git('add', 'conflict.txt')
                elif case == 'mode':
                    self.git('update-index', '--chmod=+x', 'conflict.txt')
                elif case == 'candidate_paths':
                    # A normal candidate builder accidentally included the pending plan.
                    request['resolved_candidate']['stage0_tree'] = self.git('write-tree')
                    request['candidate_tree_sha256'] = index_tree_digest(self.repo)
                elif case == 'candidate_digest':
                    # Candidate preview happened before the AI selected another resolution.
                    (self.repo / 'conflict.txt').write_text('next reviewed resolution\n')
                    self.git('add', 'conflict.txt')
                    request['resolved_candidate']['stage0_tree'] = self.git('write-tree')
                elif case == 'selected_base':
                    self.git('update-ref', 'refs/heads/main', self.old)
                elif case == 'head':
                    execute.reconcile(PACKAGE, ['--root', str(self.repo), '--request',
                                               str(self.write('before-head-change.json', request))])
                    self.git('commit', '--allow-empty', '-qm', 'normal task head advance')
                else:
                    (self.repo / '.git/sequencer').mkdir()
                before = (self.candidate_state(), self.preserved_pending_state(),
                          (self.repo / 'conflict.txt').read_bytes(),
                          (self.repo / '.git/MERGE_HEAD').read_bytes()
                          if (self.repo / '.git/MERGE_HEAD').exists() else None)
                with self.assertRaises(CommandError):
                    execute.reconcile(PACKAGE, ['--root', str(self.repo), '--request',
                                               str(self.write(case + '-post-plan.json', request))])
                after = (self.candidate_state(), self.preserved_pending_state(),
                         (self.repo / 'conflict.txt').read_bytes(),
                         (self.repo / '.git/MERGE_HEAD').read_bytes()
                         if (self.repo / '.git/MERGE_HEAD').exists() else None)
                self.assertEqual(before, after)
                self.tmp.cleanup()
                self.setUp()

    def test_post_plan_resolved_tree_preserves_selected_add_delete_and_mode(self):
        request = self.preimplementation_candidate()
        self.git('rm', '-f', 'base.txt')
        script = self.repo / 'baseline.sh'
        script.write_text('#!/bin/sh\nexit 0\n'); script.chmod(0o755)
        self.git('add', 'baseline.sh')
        self.git('update-index', '--chmod=+x', 'baseline.sh')
        with tempfile.TemporaryDirectory() as directory:
            index = Path(directory) / 'candidate-index'
            env = {**os.environ, 'GIT_INDEX_FILE': str(index)}
            subprocess.run(['git', 'read-tree', self.git('write-tree')], cwd=self.repo,
                           env=env, check=True)
            # Candidate construction restores the unselected pending plan in a temporary index.
            subprocess.run(['git', 'update-index', '--cacheinfo', '100644',
                            self.git('rev-parse', 'HEAD:task.txt'), 'task.txt'],
                           cwd=self.repo, env=env, check=True)
            request['resolved_candidate'] = {
                'stage0_tree': subprocess.run(['git', 'write-tree'], cwd=self.repo, env=env,
                    text=True, stdout=subprocess.PIPE, check=True).stdout.strip(),
                'integration_paths': ['base.txt', 'conflict.txt', 'baseline.sh']}
            request['candidate_tree_sha256'] = index_tree_digest(self.repo, index_file=index)
        before = self.preserved_pending_state()
        result = execute.reconcile(PACKAGE, ['--root', str(self.repo), '--request',
                                           str(self.write('add-delete-mode.json', request))])
        self.assertEqual(request['resolved_candidate']['stage0_tree'],
                         self.git('rev-parse', result['reconciled_task_head'] + '^{tree}'))
        self.assertEqual('', self.git('ls-tree', 'HEAD', 'base.txt'))
        self.assertTrue(self.git('ls-tree', 'HEAD', 'baseline.sh').startswith('100755 blob '))
        self.assertEqual(before, self.preserved_pending_state())

    def public_wrapper(self, package, script, *argv):
        process = subprocess.run(['bash', str(package / 'scripts' / script), '--root',
                                  str(self.repo), *argv, '--json'], cwd=SKILLS.parents[2],
                                 text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(0, process.returncode, process.stdout + process.stderr)
        value = json.loads(process.stdout)
        return value['result'] if value.get('formal_exit') is False else value

    def test_post_plan_public_transport_resumes_same_delivery_without_business_check(self):
        # Fixture semantic inputs prove owner transport only, never an AI/Phase 2 pass.
        activation = SKILLS / 'packages/guru-activate-delivery'
        projection = DeliveryProjection(self.repo, self.task_ref)
        directory = projection.planning_directory(self.delivery_key)
        for name in ('prd.md', 'design.md', 'implement.md'):
            (directory / name).write_text('当前已批准但业务尚未实施的规划\n')
        owner = self.write('activation-semantic-fixture.json', {
            'typed_exit': 'delivery_started', 'reason': 'Transport fixture after plan acceptance.'})
        projection.select(self.delivery_key)
        entries = [{'path': (directory / name).relative_to(self.repo.resolve()).as_posix(),
                    'content_sha256': hashlib.sha256((directory / name).read_bytes()).hexdigest()}
                   for name in ('prd.md', 'design.md', 'implement.md')]
        entries.sort(key=lambda entry: entry['path'])
        planning_id = 'planning:' + hashlib.sha256(json.dumps(
            entries, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
        activation_input = {'profile': 'delivery_activation', 'mode': 'workflow',
                            'task_ref': self.task_ref, 'delivery_key': self.delivery_key,
                            'planning_result_id': planning_id,
                            'action': 'activate'}
        activated = self.public_wrapper(activation, 'invoke.sh', '--input',
                                        str(self.write('activation-input.json', activation_input)),
                                        '--owner-result', str(owner))
        self.assertEqual('delivery_started', activated['exit_id'], activated)
        request = self.preimplementation_candidate()
        public = self.public('delivery_post_plan'); public['selected_base_ref'] = self.new
        public_path = self.write('post-plan-public-input.json', public)
        preview = self.public_wrapper(PACKAGE, 'execute-base-candidate.sh', '--request',
                    str(self.write('post-plan-public-preview.json', {
                        'task_head': self.head, 'new_base_head': self.new,
                        'resolved_candidate': request['resolved_candidate'],
                        'validation_commands': [['git', 'diff', '--quiet']]})))
        self.assertEqual(request['candidate_tree_sha256'], preview['candidate_tree_sha256'])
        self.assertEqual(0, preview['validations'][0]['exit_code'])
        receipt = self.public_wrapper(PACKAGE, 'execute-base-reconciliation.sh', '--request',
                                     str(self.write('post-plan-public-request.json', request)))
        recorded = self.public_wrapper(PACKAGE, 'record-base-reconciliation.sh',
                    '--skill-input', str(public_path), '--semantic-review-file',
                    str(self.write('post-plan-semantic-fixture.json', self.gate(request['candidate_tree_sha256']))),
                    '--typed-exit', 'reconciled', '--reconciliation-result',
                    str(self.write('post-plan-public-receipt.json', receipt)))
        checked = self.public_wrapper(PACKAGE, 'check-base-reconciliation.sh', '--input',
                                     str(self.write('post-plan-public-owner.json', recorded)),
                                     '--expected-exit', 'reconciled')
        self.assertEqual('ok', checked['status'])
        output = self.public_wrapper(PACKAGE, 'invoke.sh', '--invocation',
                    str(self.write('post-plan-public-invocation.json',
                                   {'public_input': public, 'owner_result': recorded})))
        self.assertEqual('delivery_activation', output['resume_target'])
        self.assertEqual(self.delivery_key, output['delivery_key'])
        self.assertEqual(self.task_ref, output['task_ref'])
        self.assertEqual(receipt['reconciled_task_head'], output['task_head'])
        activation_input['action'] = 'recover_activation'
        recovered = self.public_wrapper(activation, 'invoke.sh', '--input',
                    str(self.write('post-plan-activation-recovery.json', activation_input)),
                    '--owner-result', str(owner))
        self.assertEqual(activated, recovered)
        delivery = projection.resolve(self.delivery_key)
        self.assertEqual('implementing', delivery['phase'])
        self.assertIsNone(delivery['results']['check'])
        self.assertEqual(activated['planning_accepted_result_id'], delivery['results']['planning']['result_id'])
        self.assertEqual(1, len(json.loads((self.task_dir / 'task.json').read_text())['deliveries']))

if __name__=='__main__': unittest.main()
