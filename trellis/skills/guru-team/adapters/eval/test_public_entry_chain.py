"""Environment/transport regressions; these tests supply no native judgment."""
from __future__ import annotations

import json
import os
import shlex
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import implementation_authoring, public_entry_chain as entry
from adapters.eval import planning_authoring
from adapters.eval import public_entry_transport as transport
from adapters.eval.fixture_io import run_git
from adapters.eval.owner_runtime import load_package_runtime_module


class PublicEntryTests(unittest.TestCase):
    def template(self, root: Path) -> Path:
        template = root / 'template'
        template.mkdir()
        files = {'AGENTS.md': 'Read the installed workflow.\n',
            '.codex/config.toml': '# Original platform entry.\n',
            '.trellis/workflow.md': '# Installed workflow fixture.\n',
            '.trellis/guru-team/extension.json': '{}\n',
            '.gitignore': '.trellis/.runtime/\n',
            '.trellis/guru-team/runtime/bootstrap.py':
                'import json\nprint(json.dumps({"status":"ready"}))\n',
            '.trellis/tasks/00-bootstrap-guidelines/task.json': json.dumps({
                'id': '00-bootstrap-guidelines', 'source': {'kind': 'no_issue'},
                'deliveries': [{'id': 'init-bootstrap', 'profile': 'manual', 'phase': 'planning',
                    'plan_ref': None, 'candidate': None,
                    'results': {'planning': None, 'check': None, 'full_review': None, 'readiness': None},
                    'publication_result': None, 'delivery_result': None, 'stop_result': None}],
                'completion_results': [], 'closure_results': []})}
        for relative, content in files.items():
            path = template / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        run_git(template, 'init', '-qb', 'main')
        run_git(template, 'config', 'user.name', 'Fixture')
        run_git(template, 'config', 'user.email', 'fixture@example.invalid')
        run_git(template, 'add', '.')
        run_git(template, 'commit', '-qm', 'stage installation boundary fixture')
        return template

    def test_independent_pre_task_clones_keep_only_real_bootstrap(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            template = self.template(root)
            before = run_git(template, 'rev-parse', 'HEAD')
            for case in entry.CASES:
                prepared = entry.stage(template, root / case, case=case)
                repository = Path(prepared['repository'])
                tasks = list((repository / '.trellis/tasks').rglob('task.json'))
                self.assertEqual([json.loads(p.read_text())['id'] for p in tasks], ['00-bootstrap-guidelines'])
                self.assertEqual(tasks[0].read_bytes(),
                    (template / '.trellis/tasks/00-bootstrap-guidelines/task.json').read_bytes())
                self.assertEqual(run_git(template, 'rev-parse', 'HEAD'), before)
                state = json.loads((repository / '.trellis/.runtime/guru-team/evals/chain-provider/state.json').read_text())
                self.assertEqual(state['prs'], [])
                self.assertEqual(state['issues'][0]['state'], 'OPEN')
                self.assertNotEqual(run_git(repository, 'rev-parse', 'HEAD'), before)
                text = entry.context(prepared)
                self.assertIn('正常已安装平台入口' if case == 'N1' else 'Issue #1', text)
                self.assertNotIn('semantic-delivery-result', text)
                self.assertNotIn('planning_accepted_result_id', text)
                self.assertNotIn('expected_exit', text)
                self.assertEqual('--loss-observation' in text, case == 'N3')
            with self.assertRaisesRegex(ValueError, 'fresh run root'):
                entry.stage(template, root / 'N1', case='N1')

    def test_business_task_is_not_an_entry_precondition(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            template = self.template(root)
            task = template / '.trellis/tasks/business/task.json'
            task.parent.mkdir()
            task.write_text(json.dumps({'id': 'business', 'deliveries': []}))
            run_git(template, 'add', '.')
            run_git(template, 'commit', '-qm', 'existing business Task')
            with self.assertRaisesRegex(ValueError, 'business Task'):
                entry.stage(template, root / 'run', case='N1')

    def test_started_bootstrap_is_not_a_pre_task_template(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            template = self.template(root)
            path = template / '.trellis/tasks/00-bootstrap-guidelines/task.json'
            task = json.loads(path.read_text())
            task['deliveries'][0]['results']['planning'] = {'outcome': 'accepted'}
            path.write_text(json.dumps(task))
            run_git(template, 'add', '.')
            run_git(template, 'commit', '-qm', 'record earlier bootstrap work')
            with self.assertRaisesRegex(ValueError, 'current result'):
                entry.stage(template, root / 'run', case='N1')

    def test_author_checkout_keeps_clean_head_and_commits_actual_content(self):
        for dirty in (False, True):
            with self.subTest(dirty=dirty), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                fixture = self.template(root)
                before = run_git(fixture, 'rev-parse', 'HEAD')
                if dirty:
                    (fixture / 'business.txt').write_text('actual staged source\n')
                planning_authoring.acquire_authoring_checkout(fixture)
                after = run_git(fixture, 'rev-parse', 'HEAD')
                self.assertEqual(before == after, not dirty)
                self.assertEqual(run_git(fixture, 'branch', '--show-current'), 'eval/author')
                self.assertEqual(run_git(fixture, 'status', '--porcelain'), '')
                self.assertTrue((root / 'template-primary').is_dir())

    def test_transport_keeps_original_error_and_both_streams(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipts = root / 'commands.jsonl'
            result = transport.execute(root, receipts, [sys.executable, '-c',
                'import sys; print(sys.stdin.read()); print("diagnostic",file=sys.stderr); raise SystemExit(7)'],
                '{"ordinary":"input"}')
            self.assertEqual(result['returncode'], 7)
            self.assertEqual(result['stdout'], '{"ordinary":"input"}\n')
            self.assertEqual(result['stderr'], 'diagnostic\n')
            self.assertEqual(json.loads(receipts.read_text()), result)

    def test_provider_environment_survives_native_login_shell(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared = entry.stage(self.template(root), root / 'run', case='N1')
            repository = Path(prepared['repository'])
            receipts = root / 'login-shell.jsonl'
            prefix = [sys.executable, str(Path(transport.__file__)), '--repository', str(repository),
                '--receipts', str(receipts), '--provider-bin', prepared['provider_bin'], '--']
            command = ['gh', 'issue', 'view', '1', '--repo', 'example/stage-chain']
            provider = repository / '.trellis/.runtime/guru-team/evals/chain-provider'
            state_before = (provider / 'state.json').read_bytes()
            result = subprocess.run(['/bin/zsh', '-lc', shlex.join([*prefix, *command])],
                input='original stdin', text=True, capture_output=True, check=True)
            raw = json.loads(receipts.read_text())
            self.assertEqual(raw['argv'], command)
            self.assertEqual(raw['stdin'], 'original stdin')
            self.assertEqual(raw['returncode'], result.returncode)
            self.assertEqual(raw['stdout'], result.stdout)
            self.assertEqual(raw['stderr'], result.stderr)
            self.assertEqual(json.loads(result.stdout)['body'], entry.SOURCE)
            self.assertEqual((provider / 'state.json').read_bytes(), state_before)

            failed = ['gh', 'unsupported-local-operation']
            result = subprocess.run(['/bin/zsh', '-lc', shlex.join([*prefix, *failed])],
                input='', text=True, capture_output=True, check=False)
            raw = json.loads(receipts.read_text().splitlines()[-1])
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual((raw['returncode'], raw['stdout'], raw['stderr']),
                             (result.returncode, result.stdout, result.stderr))
            self.assertIn('Unsupported provider command', result.stderr)
            self.assertEqual((provider / 'state.json').read_bytes(), state_before)

    def test_provider_state_query_and_close_reach_original_closure_reader(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared = entry.stage(self.template(root), root / 'run', case='N1')
            repository = Path(prepared['repository'])
            provider = repository / '.trellis/.runtime/guru-team/evals/chain-provider'
            state_file = provider / 'state.json'
            receipts = root / 'closure-provider.jsonl'
            source = Path(__file__).resolve().parents[5]
            closure = load_package_runtime_module(
                source / '.trellis/guru-team/scripts/bash/run-skill-command.sh',
                'guru-complete-task-closure', 'invoke')
            issue = {'repo_ref':'example/stage-chain','issue_number':1}
            query = ['gh','issue','view','1','--repo','example/stage-chain',
                     '--json','state','--jq','.state']
            def call(argv):
                result = transport.execute(repository, receipts, argv, '', provider_bin=provider / 'bin')
                raw = json.loads(receipts.read_text().splitlines()[-1])
                self.assertEqual(raw['argv'], argv)
                self.assertEqual(raw['stdin'], '')
                self.assertEqual((raw['returncode'], raw['stdout'], raw['stderr']),
                                 (result['returncode'], result['stdout'], result['stderr']))
                self.assertEqual(result['returncode'], 0, result)
                self.assertEqual(result['stderr'], '')
                return result
            environment = {**os.environ, 'PATH':str(provider / 'bin') + os.pathsep + os.environ.get('PATH','')}
            with patch.dict(os.environ, environment, clear=True):
                for wanted in ('OPEN', 'CLOSED'):
                    before = state_file.read_bytes()
                    self.assertEqual(call(query)['stdout'], wanted + '\n')
                    self.assertEqual(closure._state(repository, issue), wanted)
                    ordinary = call(['gh','issue','view','1','--repo','example/stage-chain','--json','state'])
                    self.assertEqual(json.loads(ordinary['stdout'])['state'], wanted)
                    self.assertEqual(state_file.read_bytes(), before)
                    if wanted == 'OPEN':
                        closed = call(['gh','issue','close','1','--repo','example/stage-chain',
                                       '--reason','completed'])
                        self.assertEqual(closed['stdout'], '')

    def test_context_transport_preserves_primary_and_linked_worktree_cwd(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared = entry.stage(self.template(root), root / 'run', case='N1')
            primary = Path(prepared['repository'])
            linked = root / 'linked'
            run_git(primary, 'worktree', 'add', '-b', 'eval/cwd', str(linked), 'HEAD')
            prefix_line = next(line for line in entry.context(prepared).splitlines()
                               if prepared['transport'] in line)
            prefix = shlex.split(prefix_line)
            self.assertEqual(prefix[prefix.index('--repository') + 1], '.')
            for checkout in (primary, linked):
                result = subprocess.run([*prefix, '/bin/pwd'], cwd=checkout,
                    input='', text=True, capture_output=True, check=True)
                self.assertEqual(result.stdout.strip(), str(checkout.resolve()))
                raw = json.loads(Path(prepared['receipts']).read_text().splitlines()[-1])
                self.assertEqual(raw['argv'], ['/bin/pwd'])
                self.assertEqual((raw['returncode'], raw['stdout'], raw['stderr']),
                                 (result.returncode, result.stdout, result.stderr))

    def test_n3_loses_only_first_created_stdout_after_saving_original(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipts, loss = root / 'commands.jsonl', root / 'stdout-loss.json'
            output = {'exit_id': 'created', 'task_id': 'actual-task',
                      'task_ref': '.trellis/tasks/actual-task', 'lifecycle_generation': 0}
            wrapper = root / 'guru-create-task/scripts/invoke.sh'
            wrapper.parent.mkdir(parents=True)
            marker = root / 'creation-count.txt'
            wrapper.write_text('#!' + sys.executable + '\nfrom pathlib import Path\n'
                + 'Path(' + repr(str(marker)) + ').write_text("one creation")\n'
                + 'print(' + repr(json.dumps(output)) + ')\n')
            wrapper.chmod(0o755)
            recovery = wrapper.with_name('recover-created-task-result.sh')
            recovery.write_text('#!' + sys.executable + '\nprint(' + repr(json.dumps(output)) + ')\n')
            recovery.chmod(0o755)
            def invoke(command, *, enabled=True):
                argv = [sys.executable, str(Path(transport.__file__)), '--repository', str(root),
                        '--receipts', str(receipts)]
                if enabled:
                    argv += ['--loss-observation', str(loss)]
                return subprocess.run([*argv, '--', str(command)], input='',
                    capture_output=True, text=True, check=True)
            # N1/N2 retain their ordinary delivery behavior.
            visible = invoke(recovery, enabled=False)
            self.assertEqual(json.loads(visible.stdout), output)
            self.assertFalse(loss.exists())
            first = invoke(wrapper)
            self.assertEqual(first.stdout, '')
            self.assertEqual(first.returncode, 0)
            saved = [json.loads(line) for line in receipts.read_text().splitlines()]
            self.assertEqual(json.loads(saved[1]['stdout']), output)
            self.assertEqual(json.loads(loss.read_text()), {'receipt_index': 1,
                'producer': 'guru-create-task', 'stdout_delivered': False})
            recovered = invoke(recovery)
            self.assertEqual(json.loads(recovered.stdout), output)
            self.assertEqual(marker.read_text(), 'one creation')
            self.assertEqual(len(receipts.read_text().splitlines()), 3)

    def test_loss_does_not_consume_mode_or_failed_producer_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            receipts, loss = root / 'commands.jsonl', root / 'stdout-loss.json'
            for skill, code, output in (
                    ('guru-select-workflow-mode', 0, {'exit_id': 'standard_intake'}),
                    ('guru-create-task', 2, {'code': 'schema_mismatch'}),
                    ('guru-create-delivery', 0, {'exit_id': 'blocked'})):
                argv = [sys.executable, '-c', 'import sys; print(sys.argv[1]); raise SystemExit(int(sys.argv[2]))',
                        json.dumps(output), str(code), '/public/' + skill + '/scripts/invoke.sh']
                result = transport.execute(root, receipts, argv, '')
                self.assertEqual(transport.delivered_stdout(result, receipts, loss), result['stdout'])
                self.assertFalse(loss.exists())

    def test_provider_observes_issue_close_and_file_based_pr_body(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            prepared = entry.stage(self.template(root), root / 'run', case='N1')
            repository = Path(prepared['repository'])
            gh = Path(prepared['provider_bin']) / 'gh'
            def call(*args):
                return subprocess.run([str(gh), *args], cwd=repository, text=True,
                    capture_output=True, check=True).stdout
            issue = json.loads(call('issue', 'view', '1', '--repo', 'example/stage-chain'))
            self.assertEqual(issue['body'], entry.SOURCE)
            call('issue', 'close', '1', '--repo', 'example/stage-chain', '--reason', 'completed')
            self.assertEqual(json.loads(call('issue', 'view', issue['url']))['state'], 'CLOSED')
            body = root / 'body.md'
            body.write_text('Reviewed provider payload.\n')
            run_git(repository, 'push', 'origin', 'HEAD:refs/heads/feature')
            call('pr', 'create', '--head', 'feature', '--base', 'main', '--title', 'Test', '--body-file', str(body))
            row = json.loads(call('pr', 'view', '1'))
            self.assertEqual(row['body'], body.read_text())

    def test_provider_merge_preserves_inline_and_file_message_bodies(self):
        for carrier in ("--body", "--body-file"):
            with self.subTest(carrier=carrier), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                prepared = entry.stage(self.template(root), root / "run", case="N1")
                repository = Path(prepared["repository"])
                provider = Path(prepared["provider_bin"]).parent
                bare = provider / "remote.git"
                gh = provider / "bin/gh"
                def call(*args):
                    return subprocess.run([str(gh), *args], cwd=repository, text=True,
                                          capture_output=True, check=True).stdout
                before = run_git(repository, "rev-parse", "HEAD")
                (repository / "bookkeeping.md").write_text("Actual local bookkeeping.\n")
                run_git(repository, "add", "--", "bookkeeping.md")
                run_git(repository, "commit", "-qm", "bookkeeping candidate")
                head = run_git(repository, "rev-parse", "HEAD")
                run_git(repository, "push", "origin", "HEAD:refs/heads/bookkeeping")
                call("pr", "create", "--head", "bookkeeping", "--base", "main",
                     "--title", "Bookkeeping", "--body", "Refs #1")
                body = "Preserve this merge body.\n\nTask history stays complete."
                body_file = root / "merge-body.md"
                body_file.write_text(body)
                call("pr", "merge", "1", "--merge", "--match-head-commit", head,
                     "--subject", "Complete bookkeeping", carrier,
                     str(body_file) if carrier == "--body-file" else body)
                row = json.loads(call("pr", "view", "1"))
                merged = row["mergeCommit"]["oid"]
                self.assertEqual(row["state"], "MERGED")
                self.assertEqual(run_git(repository, "--git-dir", str(bare), "show", "-s", "--format=%P", merged).split(), [before, head])
                self.assertEqual(run_git(repository, "--git-dir", str(bare), "show", "-s", "--format=%B", merged).strip(), "Complete bookkeeping\n\n" + body)

    def test_candidate_observation_relays_public_producer_not_private_identity(self):
        key = {'task_id': 't', 'lifecycle_generation': 0, 'delivery_id': 'd'}
        candidate = {'kind': 'git', 'content_ref': 'sha256:public-producer',
                     'paths': ['app.py'], 'head_ref': 'a' * 40, 'base_ref': 'b' * 40}
        current = {'kind': 'current', 'key': key, 'delivery': {'candidate': candidate}}
        content = {'algorithm': 'guru-reviewed-content-1.0', 'sha256': 'c' * 64,
                   'commit': 'a' * 40, 'include_worktree': True}
        facts = {'task_ref': '.trellis/tasks/t', 'delivery_key': key,
                 'planning_root': '.trellis/tasks/t/deliveries/d', 'original_candidate': {}}
        responses = iter([current, candidate, {'result': content}])
        calls = []
        environments = []
        def command(argv, **kwargs):
            calls.append(argv)
            environments.append(kwargs['env'])
            return subprocess.CompletedProcess(argv, 0, json.dumps(next(responses)), '')
        with patch.object(implementation_authoring.subprocess, 'run', side_effect=command), \
                patch.object(implementation_authoring, 'run_git', return_value='a' * 40), \
                patch('adapters.eval.eval_support.qualification_planning_identity', return_value='e' * 64):
            observed = implementation_authoring.observe_candidate(Path('/isolated'), facts, ['app.py'],
                environment={'TRELLIS_CONTEXT_ID': 'isolated-caller', 'PATH': '/fixture/bin'})
        self.assertEqual(observed['candidate'], candidate)
        self.assertEqual(observed['reviewed_content'], content)
        self.assertNotIn('reviewed_content_sha256', observed)
        self.assertIn('construct-delivery-candidate.sh', calls[1][1])
        self.assertIn('reviewed_content_identity', calls[2])
        self.assertTrue(all(env['TRELLIS_CONTEXT_ID'] == 'isolated-caller' for env in environments))
        self.assertTrue(all(env['PATH'] == '/fixture/bin' for env in environments))


if __name__ == '__main__':
    unittest.main()
