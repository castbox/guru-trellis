"""Exercise current API staging and original command transport, not AI outcomes."""
from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import native_adapter, stage_result_authoring as stage
from runtime.delivery_projection.adapter import DeliveryProjection

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]


def request(root, skill, case):
    package = SKILLS / 'packages' / skill
    row = next(row for row in json.loads((package / 'evals/evals.json').read_text())['evals']
               if row['id'] == 'native-stage-' + case)
    workdir = root / 'execution/workdir'
    workdir.mkdir(parents=True)
    for relative in row['files']:
        target = workdir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(package / relative, target)
    interface = json.loads((package / 'interface.json').read_text())
    return {'schema_version': '1.0', 'skill_id': skill, 'package_root': str(package),
        'case_id': row['id'], 'prompt': row['prompt'], 'files': row['files'], 'workdir': str(workdir),
        'interface': {'public_invocation': interface['public_contracts']['invocation']},
        'runtime_target': str(REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh'),
        'native_execution_mode': 'semantic_authoring', 'native_execution_adapter': 'codex',
        'model_id': row['model_id']}


class StageResultTransportTests(unittest.TestCase):
    def transport_fixture(self, *, planning=False):
        from adapters.eval.fixture_io import stage_clean_installed_owner_repo
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        package = REPO / '.trellis/guru-team/skills/packages/guru-review-task-completion'
        owner, source = stage_clean_installed_owner_repo(root,
            REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', package)
        if planning:
            from adapters.eval import stage_result_chain as chain
            req = request(root, 'guru-review-task-completion', 'p04')
            req['case_id'] = chain.CASE
            chain.stage(req, owner, owner / '.trellis/guru-team/skills/packages' / package.name, source)
        else:
            stage.write_json(owner / stage.FACTS, {'writable_paths': []})
        (owner / '.trellis/.runtime/guru-team/evals').mkdir(parents=True, exist_ok=True)
        facts = json.loads((owner / stage.FACTS).read_text())
        from adapters.eval.architecture_authoring import DELIVERY_CONTEXT
        environment = {**os.environ,
            'TRELLIS_CONTEXT_ID': os.environ.get('TRELLIS_CONTEXT_ID') or DELIVERY_CONTEXT}
        relay = stage.ImplementationCommands(owner, environment, root / 'receipts.json')
        return owner, facts, relay

    def owner_command(self, relay, skill, command, arguments, value=None, *, expected=0):
        result = relay.forward({'skill_id': skill, 'command': command,
            'arguments': arguments, 'stdin': json.dumps(value) if value is not None else ''})
        self.assertEqual(result['returncode'], expected, result)
        return json.loads(result['stdout'])

    def test_wording_invocation_retires_only_successful_file_inputs(self):
        owner, _, relay = self.transport_fixture()
        skill = 'guru-review-contract-wording'
        package = owner / '.trellis/guru-team/skills/packages' / skill
        (owner / 'contract.md').write_text('Exact contract.\n')
        selectors = ['--profile', 'explicit_paths', '--mode', 'standalone', '--path', 'contract.md']
        scan = self.owner_command(relay, skill, 'record-contract-wording-review',
            [*selectors, '--scan-only'])['result']
        example = json.loads((package / 'examples/contract-wording-review.json').read_text())
        review = example['semantic_review']
        review['ai_review_gate'].pop('planning_checked_dimensions')
        review['ai_review_gate'].update(reviewed_scan_sha256=scan['scan']['scan_sha256'],
            summary='Deterministic transport probe; no native review claim.')
        authored = {'generated_at': example['generated_at'], 'typed_exit': 'pass',
            'revisions': [], 'classifications': [], 'ai_review_gate': review['ai_review_gate']}
        recorded = self.owner_command(relay, skill, 'record-contract-wording-review',
            [*selectors, '--input', '-'], authored)['result']
        checked = self.owner_command(relay, skill, 'check-contract-wording-review',
            ['--path', 'contract.md', '--input', '-'], recorded)['result']
        public = json.loads((package / 'examples/public-explicit-paths-input.json').read_text())
        public['paths'] = ['contract.md']
        envelope = {'public_input': public, 'owner_result': recorded,
            'validation_receipt': checked['validation_receipt']}
        runtime = owner / '.trellis/.runtime/guru-team/evals'
        unused = runtime / 'unused-wording.json'
        unused.write_text('{}')
        for transport in ('file', 'stdin'):
            with self.subTest(transport=transport):
                path = runtime / 'wording-invocation.json'
                path.write_text(json.dumps(envelope))
                argument = path.relative_to(owner).as_posix() if transport == 'file' else '-'
                output = self.owner_command(relay, skill, 'invoke-' + skill,
                    ['--invocation', argument], envelope if transport == 'stdin' else None)
                self.assertEqual(output['exit_id'], 'pass')
                self.assertEqual(path.exists(), transport != 'file')
        path.write_text(json.dumps({'public_input': public}))
        self.owner_command(relay, skill, 'invoke-' + skill,
            ['--invocation', str(path)], expected=2)
        self.assertTrue(path.is_file())
        self.assertTrue(unused.is_file())

    def test_intermediate_file_consumers_retire_only_their_completed_inputs(self):
        from unittest.mock import patch
        owner, _, relay = self.transport_fixture()
        runtime = owner / '.trellis/.runtime/guru-team/evals'
        unused = runtime / 'unconsumed.json'
        unused.write_text('{}')
        calls = (
            ('guru-review-branch', 'review-branch', ('--semantic-review-file',)),
            ('guru-check-task', 'record-phase2-check', ('--input',)),
            ('guru-create-task-commit', 'prepare-task-commit', ('--input', '--candidate-json')),
        )
        for skill, command, flags in calls:
            with self.subTest(command=command):
                paths = [runtime / (command + str(index) + '.json')
                         for index in range(len(flags))]
                arguments = []
                for flag, path in zip(flags, paths):
                    path.write_text('{}')
                    arguments.extend((flag, str(path)))
                # Stub only the external wrapper process. The real relay still
                # discovers the declared command and handles its returned receipt.
                response = subprocess.CompletedProcess([], 0,
                    json.dumps({'schema_version': '1.0', 'formal_exit': False,
                                'result': {'status': 'recorded'}}), '')
                with patch.object(stage.implementation.subprocess, 'run', return_value=response):
                    result = relay.forward({'skill_id': skill, 'command': command,
                        'arguments': arguments, 'stdin': ''})
                self.assertEqual(result['returncode'], 0)
                self.assertTrue(all(not path.exists() for path in paths))
                self.assertTrue(all(path.relative_to(owner).as_posix() in relay.consumed_paths
                                    for path in paths))
        self.assertTrue(unused.is_file())

    def test_failed_or_preview_consumers_preserve_input_bytes(self):
        from unittest.mock import patch
        owner, _, relay = self.transport_fixture()
        path = owner / '.trellis/.runtime/guru-team/evals/check-authoring.json'
        original = b'{"transport_probe": true}\n'
        cases = (
            (3, '{"code":"stale_identity"}', []),
            (0, '{"request_error":"invalid operation","returncode":2}', []),
            (0, 'usage: record-phase2-check', ['--help']),
            (0, '{"result":{"dry_run":true}}', ['--dry-run']),
        )
        for returncode, stdout, extra in cases:
            with self.subTest(returncode=returncode, extra=extra):
                path.write_bytes(original)
                response = subprocess.CompletedProcess([], returncode, stdout, '')
                with patch.object(stage.implementation.subprocess, 'run', return_value=response):
                    relay.forward({'skill_id': 'guru-check-task', 'command': 'record-phase2-check',
                        'arguments': ['--input', str(path), *extra], 'stdin': ''})
                self.assertEqual(path.read_bytes(), original)
                self.assertNotIn(path.relative_to(owner).as_posix(), relay.consumed_paths)

    def test_original_delivery_api_retires_success_and_preserves_failed_reentry(self):
        import hashlib
        from adapters.eval.architecture_authoring import DELIVERY_CONTEXT
        with tempfile.TemporaryDirectory() as temporary:
            req = request(Path(temporary), 'guru-check-task', 'c01')
            values = native_adapter.build_context(req, 'codex')
            try:
                protocol = json.loads(values[4].read_text())
                owner = Path(protocol['owner_repository'])
                public = json.loads((owner / 'docs/phase2-evidence/check-public-input.json').read_text())
                facts = {'task_ref': public['task_ref'], 'writable_paths': []}
                stage.write_json(owner / stage.FACTS, facts)
                projection = DeliveryProjection(owner, facts['task_ref'])
                key = public['delivery_key']
                delivery = projection.resolve(key)
                reason_path = projection.planning_directory(key) / 'implement.md'
                reason = {'locator': reason_path.relative_to(owner).as_posix(),
                          'revision': 'sha256:' + hashlib.sha256(reason_path.read_bytes()).hexdigest()}
                relay = stage.ImplementationCommands(owner,
                    {**os.environ, 'TRELLIS_CONTEXT_ID': os.environ.get('TRELLIS_CONTEXT_ID') or DELIVERY_CONTEXT},
                    Path(temporary) / 'api-receipts.json')
                runtime = owner / '.trellis/.runtime/guru-team/evals'
                runtime.mkdir(parents=True, exist_ok=True)
                rework = runtime / 'rework.json'
                stage.write_json(rework, {'api_version': '1.0', 'operation': 'rework',
                    'key': key, 'owner_role': 'check',
                    'owner_id': projection.declaration()['owners']['check'],
                    'expected_phase': 'checking', 'target_role': 'implementation',
                    'reason': reason, 'affected_results': ['check', 'full_review', 'readiness']})
                self.owner_command(relay, 'delivery-api', 'rework',
                    ['--task', facts['task_ref'], '--input', str(rework)])
                self.assertFalse(rework.exists())
                self.assertEqual(projection.resolve(key)['phase'], 'implementing')
                begin = runtime / 'begin-check.json'
                operation = {'api_version': '1.0', 'operation': 'begin_check',
                    'key': key, 'owner_role': 'implementation',
                    'owner_id': projection.declaration()['owners']['implementation'],
                    'expected_phase': 'implementing', 'candidate': delivery['candidate']}
                stage.write_json(begin, operation)
                self.owner_command(relay, 'delivery-api', 'begin-check',
                    ['--task', facts['task_ref'], '--input', str(begin)])
                self.assertFalse(begin.exists())
                self.assertEqual(projection.resolve(key)['phase'], 'checking')
                stage.write_json(begin, operation)
                original = begin.read_bytes()
                failed = relay.forward({'skill_id': 'delivery-api', 'command': 'begin-check',
                    'arguments': ['--task', facts['task_ref'], '--input', str(begin)], 'stdin': ''})
                self.assertNotEqual(failed['returncode'], 0)
                self.assertEqual(begin.read_bytes(), original)
            finally:
                values[9].set()
                values[8].join(timeout=2)

    def test_publication_files_remain_intact_and_unknown_inventory_still_fails(self):
        import importlib.util
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch
        from adapters.eval import stage_result_chain as chain
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            req = request(root, 'guru-review-task-completion', 'p04')
            req['case_id'] = chain.CASE
            request_path = root / 'request.json'
            stage.write_json(request_path, req)
            values = native_adapter.build_context(req, 'codex')
            protocol = json.loads(values[4].read_text())
            owner = Path(protocol['owner_repository'])
            facts = json.loads((owner / stage.FACTS).read_text())
            source = owner / '.trellis/guru-team/skills/packages/guru-publish-task-delivery/runtime/owner.py'
            spec = importlib.util.spec_from_file_location('publication_inventory_probe', source)
            publisher = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(publisher)
            public = {'profile': 'delivery_review_ready', 'task_ref': facts['task_ref'],
                      'delivery_key': facts['delivery_key'], 'readiness_result_id': 'readiness:transport-probe'}
            reference = publisher.transaction_ref(public)
            originals = {}
            unexpected = []
            unknown = owner / '.trellis/.runtime/guru-team/evals/unknown-output.json'
            original_run = subprocess.run

            def native_process(argv, **kwargs):
                if len(argv) > 1 and argv[1] == 'exec':
                    # Exercise the original private writers and identity producer.
                    # This is an inventory probe, not a native semantic assessment.
                    publisher.save_transaction(owner, {'schema_version': '2.0',
                        'skill_id': publisher.SKILL_ID, 'transaction_ref': reference,
                        'input': public, 'action': 'ready', 'terminal': 'ready', 'stage': 'ready'})
                    transaction = publisher.transaction_path(owner, reference)
                    gate = publisher.record_gate(owner, {'transaction_ref': reference,
                        'confirmation_identity': 'transport-plan-identity'}, {'review': {}, 'route': {}})
                    originals.update({path: path.read_bytes() for path in (transaction, gate)})
                    unknown.write_text('{}')
                    # A normal output for another Task is outside this execution.
                    other = {**public, 'task_ref': '.trellis/tasks/another-task',
                        'delivery_key': {**facts['delivery_key'], 'task_id': 'another-task'}}
                    other_ref = publisher.transaction_ref(other)
                    publisher.save_transaction(owner, {'schema_version': '2.0',
                        'skill_id': publisher.SKILL_ID, 'transaction_ref': other_ref,
                        'input': other, 'action': 'ready', 'terminal': 'ready', 'stage': 'ready'})
                    unexpected.append(publisher.transaction_path(owner, other_ref))
                    return subprocess.CompletedProcess(argv, 0, '{}', '')
                return original_run(argv, **kwargs)

            output = io.StringIO()
            try:
                with patch.object(sys, 'argv', ['native_adapter', '--adapter', 'codex',
                        '--native-command', sys.executable, '--request', str(request_path)]), \
                     patch.object(native_adapter, 'build_context', return_value=values), \
                     patch.object(native_adapter, 'prepare_isolated_codex_permissions', return_value=(None, [])), \
                     patch.object(native_adapter, 'run_codex_permission_probe', return_value={'returncode': 0}), \
                     patch.object(native_adapter.subprocess, 'run', side_effect=native_process), \
                     redirect_stdout(output):
                    native_adapter.main()
                response = json.loads(output.getvalue())
                self.assertEqual(response['capability_status'], 'execution_error')
                self.assertEqual(response['public_stderr'],
                    'isolated Codex authoring changed repository file inventory')
                transcript = json.loads((root / 'adapter-transcript.json').read_text())
                self.assertEqual(transcript['repository_changed_paths'],
                    sorted(path.relative_to(owner).as_posix() for path in [unknown, *unexpected]))
                self.assertEqual(len(originals), 2)
                for path, content in originals.items():
                    self.assertEqual(path.read_bytes(), content)
            finally:
                values[9].set()
                values[8].join(timeout=2)

    def test_planning_recorder_input_retires_after_its_checkpoint_is_consumed(self):
        import hashlib
        for resume in (False, True):
            with self.subTest(resume=resume):
                owner, facts, relay = self.transport_fixture(planning=True)
                skill = 'guru-approve-task-plan'
                package = owner / '.trellis/guru-team/skills/packages' / skill
                directory = DeliveryProjection(owner, facts['task_ref']).planning_directory(facts['delivery_key'])
                for name in ('prd.md', 'design.md', 'implement.md'):
                    (directory / name).write_text('Exact plan.\n')
                example = json.loads((package / 'examples/planning-approval-delivery.json').read_text())
                semantic = {name: example[name] for name in ('mode', 'authority_refs',
                    'delivery_policy', 'docs_ssot_plan', 'semantic_review', 'typed_exit', 'consumer', 'reason')}
                runtime = owner / '.trellis/.runtime/guru-team/evals'
                source = runtime / 'approval-semantic.json'
                source.write_text(json.dumps(semantic))
                selectors = ['--task', facts['task_ref'], '--delivery-key', json.dumps(facts['delivery_key'])]
                earlier = runtime / 'earlier-approval-semantic.json'
                earlier.write_text(json.dumps(semantic))
                self.owner_command(relay, skill, 'record-planning-approval',
                    [*selectors, '--input', str(earlier)])
                recorded = self.owner_command(relay, skill, 'record-planning-approval',
                    [*selectors, '--input', str(source)])['result']
                self.assertTrue(source.is_file())
                self.owner_command(relay, skill, 'check-planning-approval', selectors)
                self.assertTrue(source.is_file())
                public = json.loads((package / 'examples/public-delivery-initial-review-input-2.0.json').read_text())
                public.update(task_ref=facts['task_ref'], delivery_key=facts['delivery_key'])
                public['architecture_assessment']['freshness_identity'] = 'sha256:' + hashlib.sha256(
                    (directory / 'design.md').read_bytes()).hexdigest()
                public_file = runtime / 'approval-public.json'
                public_file.write_text(json.dumps(public))
                arguments = ['--input', str(public_file), '--owner-result', recorded['artifact_path']]
                if resume:
                    (directory / 'design.md').write_text('Ordinary stale plan edit.\n')
                    self.owner_command(relay, skill, 'invoke', arguments, expected=3)
                    self.assertTrue(source.is_file())
                    self.assertTrue(Path(recorded['artifact_path']).is_file())
                    # Reuse actual preceding responses in the continuation shape
                    # produced by stage_result_chain.resume_execution.
                    continuation = '.trellis/tasks/stage-result-evidence/continuation.json'
                    stage.write_json(owner / continuation, {'preceding_commands': relay.receipts})
                    facts['continuation_locator'] = continuation
                    stage.write_json(owner / stage.FACTS, facts)
                    relay = stage.ImplementationCommands(owner, relay.environment,
                        relay.receipts_path.with_name('resumed-receipts.json'))
                    (directory / 'design.md').write_text('Exact plan.\n')
                unused = runtime / 'unconsumed-semantic.json'
                unused.write_text(json.dumps(semantic))
                output = self.owner_command(relay, skill, 'invoke', arguments)
                self.assertEqual(output['exit_id'], 'approved')
                self.assertFalse(Path(recorded['artifact_path']).exists())
                self.assertFalse(source.exists())
                self.assertTrue(earlier.is_file())
                self.assertTrue(unused.is_file())
                self.assertIn(source.relative_to(owner).as_posix(), relay.consumed_paths)

    def test_installed_fixture_includes_required_live_specs(self):
        from adapters.eval.fixture_io import stage_clean_installed_owner_repo
        with tempfile.TemporaryDirectory() as temporary:
            fixture, source = stage_clean_installed_owner_repo(Path(temporary),
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh',
                REPO / '.trellis/guru-team/skills/packages/guru-review-task-completion')
            for name in ('clear-technical-writing.md', 'workflow-contract.md'):
                relative = Path('.trellis/spec/workflow') / name
                self.assertEqual((fixture / relative).read_bytes(), (source / relative).read_bytes())

    def test_raw_observations_stay_readable_outside_reviewed_business_content(self):
        from adapters.eval import stage_result_chain as chain
        from adapters.eval.eval_support import stage_repository_projection
        from adapters.eval.fixture_io import run_git
        from runtime.reviewed_content import reviewed_content_identity
        owner, facts, _ = self.transport_fixture(planning=True)
        exclude = owner / run_git(owner, 'rev-parse', '--git-path', 'info/exclude')
        previous = exclude.read_bytes() + b'# Existing local test configuration'
        exclude.write_bytes(previous)
        chain.configure_raw_observation_paths(owner)
        configured = exclude.read_bytes()
        self.assertTrue(configured.startswith(previous))
        chain.configure_raw_observation_paths(owner)
        self.assertEqual(exclude.read_bytes(), configured)
        before = reviewed_content_identity(owner)
        observations = {}
        for relative in (*chain.RAW_OBSERVATION_PATHS, *chain.CARRIER_PATHS):
            path = owner / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            observations[relative] = (path.read_bytes() if path.exists()
                else ('Raw transport probe: ' + relative + '\n').encode())
            path.write_bytes(observations[relative])
            self.assertEqual(run_git(owner, 'check-ignore', relative), relative)
        self.assertEqual(reviewed_content_identity(owner), before)
        self.assertNotIn('docs/chain-evidence/', run_git(owner, 'status', '--porcelain'))
        public = owner.parent / 'raw-observation-projection'
        stage_repository_projection(owner, public)
        for relative, content in observations.items():
            self.assertEqual((public / relative).read_bytes(), content)
        business = owner / 'docs/current-usage.md'
        business.write_text('Changed business guidance must remain in reviewed content.\n')
        self.assertIn('docs/current-usage.md', run_git(owner, 'status', '--porcelain'))
        self.assertNotEqual(reviewed_content_identity(owner), before)
        task_scope = facts['task_ref'] + '/prd.md'
        projection = DeliveryProjection(owner, facts['task_ref'])
        task_candidate = projection.candidate([task_scope])
        with (owner / task_scope).open('a') as stream:
            stream.write('\nChanged Task authority must remain in reviewed content.\n')
        self.assertIn(task_scope, run_git(owner, 'status', '--porcelain'))
        self.assertNotEqual(projection.candidate([task_scope])['content_ref'], task_candidate['content_ref'])

    def test_continuous_fixture_has_no_semantic_gates_and_provider_merges_real_git(self):
        with tempfile.TemporaryDirectory() as temporary:
            req = request(Path(temporary), 'guru-review-task-completion', 'p04')
            from adapters.eval import stage_result_chain as chain
            req['case_id'] = chain.CASE
            values = native_adapter.build_context(req, 'codex')
            try:
                protocol = json.loads(values[4].read_text())
                for command in values[0].splitlines()[1:4]:
                    argv = shlex.split(command)
                    read = subprocess.run(argv, check=True, capture_output=True)
                    target = Path(argv[argv.index('--path') + 1])
                    self.assertEqual(read.stdout, target.read_bytes())
                owner = Path(protocol['owner_repository'])
                from runtime.task_lifecycle.identity import origin_matches
                self.assertTrue(origin_matches(owner, 'example/stage-chain'))
                facts = json.loads((owner / stage.FACTS).read_text())
                projection = DeliveryProjection(owner, facts['task_ref'])
                self.assertEqual(projection.read_record()['completion_results'], [])
                delivery = projection.resolve(facts['delivery_key'])
                self.assertEqual(facts['planning_root'], delivery['planning_root'])
                self.assertEqual(delivery['phase'], 'planning')
                self.assertTrue(all(value is None for value in delivery['results'].values()))
                self.assertIsNone(delivery['delivery_result'])
                self.assertFalse((owner / stage.ARCHITECTURE_PREREQUISITE).exists())
                relay = stage.ImplementationCommands(owner, dict(os.environ),
                    Path(temporary) / 'write-receipts.json', facts_relative=stage.FACTS)
                invalid = relay.forward({'skill_id': 'guru-author-task-plan', 'command': 'help',
                    'arguments': [], 'stdin': ''})
                self.assertEqual(json.loads(invalid['stdout'])['returncode'], 2)
                self.assertFalse(relay.terminal)
                transient = '.trellis/.runtime/guru-team/evals/command-input.json'
                rejected = relay.forward({'skill_id': 'implementation-authoring', 'command': 'write',
                    'arguments': [], 'stdin': json.dumps({'file_updates': {transient: '{}'}})})
                self.assertEqual(json.loads(rejected['stdout'])['returncode'], 2)
                self.assertFalse(relay.terminal)
                self.assertFalse((owner / transient).exists())
                corrected = relay.forward({'skill_id': 'implementation-authoring', 'command': 'run',
                    'arguments': [], 'stdin': json.dumps({'argv': [sys.executable, '-c',
                        'from pathlib import Path; p=Path(' + repr(transient) + '); p.parent.mkdir(parents=True,exist_ok=True); p.write_text("{}")']})})
                self.assertEqual(json.loads(corrected['stdout'])['returncode'], 0)
                self.assertEqual((owner / transient).read_text(), '{}')
                (owner / transient).unlink()
                planning = facts['task_ref'] + '/' + facts['planning_root'] + '/prd.md'
                written = relay.forward({'skill_id': 'implementation-authoring', 'command': 'write',
                    'arguments': [], 'stdin': json.dumps({'file_updates': {planning: '# Owner-authored plan\n'}})})
                self.assertEqual(written['returncode'], 0)
                self.assertEqual((owner / planning).read_text(), '# Owner-authored plan\n')
                self.assertIsNone(projection.resolve(facts['delivery_key'])['results']['planning'])

                def git(*argv):
                    return subprocess.check_output(['git', *argv], cwd=owner, text=True).strip()
                from adapters.eval.eval_support import repository_file_inventory
                before_provider = repository_file_inventory(owner)
                head0 = git('rev-parse', 'HEAD')
                (owner/'contract.txt').write_text('Actual provider merge probe.\n')
                git('add', 'contract.txt');git('commit','-qm','provider I/O test')
                head = git('rev-parse','HEAD')
                git('push','origin','HEAD:refs/heads/probe')
                gh = Path(facts['provider_bin'])/'gh'
                repository = subprocess.run([str(gh), 'repo', 'view', '--json', 'nameWithOwner'],
                    cwd=owner, check=True, capture_output=True, text=True)
                self.assertEqual(json.loads(repository.stdout), {'nameWithOwner': 'example/stage-chain'})
                subprocess.run([str(gh),'pr','create','--head','probe','--base','main',
                    '--title','probe','--body','I/O only'],cwd=owner,check=True,capture_output=True)
                body = owner/'.trellis/.runtime/guru-team/evals/merge-body.txt';body.write_text('Exact body.')
                subprocess.run([str(gh),'pr','merge','1','--merge','--match-head-commit',head,
                    '--subject','Exact subject','--body-file',str(body)],cwd=owner,check=True,capture_output=True)
                git('fetch','origin','main')
                parents = git('show','-s','--format=%P','origin/main').split()
                self.assertEqual(parents,[head0,head])
                self.assertEqual(git('show','-s','--format=%B','origin/main'),'Exact subject\n\nExact body.')
                self.assertIsNone(projection.resolve(facts['delivery_key'])['delivery_result'])
                after_provider = repository_file_inventory(owner)
                provider_prefix = str(Path(facts['provider_bin']).parent.relative_to(owner)) + '/'
                provider_changes = {path for path in before_provider.keys() | after_provider.keys()
                    if path.startswith(provider_prefix)
                    and before_provider.get(path) != after_provider.get(path)}
                self.assertTrue(provider_changes)
                self.assertTrue(provider_changes <= set(stage.additional_mutated_paths(owner, facts)))

                # This unit probe exercises the enumerator's current Task path.
                # Actual TaskCommit producer evidence comes from the native chain.
                commit_result = owner / '.trellis/.runtime/guru-team/task-commit-results' / Path(facts['task_ref']).name / '001.json'
                commit_result.parent.mkdir(parents=True, exist_ok=True)
                commit_result.write_text('{}')
                allowed = set(stage.additional_mutated_paths(owner, facts))
                self.assertIn(commit_result.relative_to(owner).as_posix(), allowed)
                self.assertNotIn(gh.relative_to(owner).as_posix(), allowed)
                self.assertNotIn(body.relative_to(owner).as_posix(), allowed)

                original_read = {'skill_id': 'delivery-api', 'command': 'contract',
                    'arguments': ['--json'], 'stdin': ''}
                original_output = relay.forward(original_read)
                self.assertEqual(original_output['returncode'], 0)
                original_call = {'skill_id': 'guru-author-task-plan', 'command': 'invoke',
                    'arguments': ['--input', '{}', '--owner-result', '{}'], 'stdin': ''}
                failed = relay.forward(original_call)
                self.assertNotEqual(failed['returncode'], 0)
                planning_before = (owner / planning).read_bytes()
                after_terminal = relay.forward({'skill_id': 'implementation-authoring', 'command': 'write',
                    'arguments': [], 'stdin': json.dumps({'file_updates': {planning: '# Repeated write\n'}})})
                terminal_error = json.loads(after_terminal['stdout'])
                self.assertEqual(terminal_error['returncode'], 2)
                self.assertIn('terminal original wrapper', terminal_error['request_error'])
                self.assertEqual((owner / planning).read_bytes(), planning_before)
                protocol['implementation_receipts_path'] = str(relay.receipts_path)
                values[4].write_text(json.dumps(protocol))
                transcript = Path(protocol['native_request_path']).parent / 'adapter-transcript.json'
                transcript.write_text(json.dumps({'returncode': 0}))
                from unittest.mock import patch
                with patch.dict(os.environ, {chain.RESUME_PROTOCOL_ENV: str(values[4])}):
                    chain.resume_execution(req)
                resumed = json.loads((owner / stage.FACTS).read_text())
                continuation = json.loads((owner / resumed['continuation_locator']).read_text())
                preserved = next(row for row in continuation['preceding_commands']
                    if row['request']['command'] == 'invoke')
                self.assertEqual(preserved['request'], original_call)
                self.assertEqual(preserved['response'], failed)
                second = stage.ImplementationCommands(owner, dict(os.environ),
                    Path(temporary) / 'second-receipts.json', facts_relative=stage.FACTS)
                second_call = {'skill_id': 'delivery-api', 'command': '--help',
                    'arguments': [], 'stdin': ''}
                second_output = second.forward(second_call)
                self.assertEqual(second_output['returncode'], 0)
                protocol['implementation_receipts_path'] = str(second.receipts_path)
                values[4].write_text(json.dumps(protocol))
                with patch.dict(os.environ, {chain.RESUME_PROTOCOL_ENV: str(values[4])}):
                    chain.resume_execution(req)
                continued = json.loads((owner / resumed['continuation_locator']).read_text())
                commands = continued['preceding_commands']
                self.assertEqual(commands, [*continuation['preceding_commands'],
                    {'request': second_call, 'response': second_output}])
                self.assertIn({'request': original_read, 'response': original_output}, commands)
                self.assertIn({'request': original_call, 'response': failed}, commands)
                self.assertEqual(projection.read_record()['completion_results'], [])
                self.assertIsNone(projection.resolve(facts['delivery_key'])['delivery_result'])
            finally:
                values[9].set(); values[8].join(timeout=2)

    def interrupted_fixture(self):
        """Execute a real read-only owner command, then leave the segment partial."""
        from adapters.eval import stage_result_chain as chain
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        req = request(Path(temporary.name), 'guru-review-task-completion', 'p04')
        req['case_id'] = chain.CASE
        values = native_adapter.build_context(req, 'codex')
        self.addCleanup(lambda: values[8].join(timeout=2))
        self.addCleanup(values[9].set)
        protocol = json.loads(values[4].read_text())
        # Use the native helper and its actual relay, including stdout normalization.
        read = shlex.split(values[0].splitlines()[1])
        subprocess.run(read, check=True, capture_output=True)
        prefix = read[:read.index('read')]
        result = subprocess.run([*prefix, 'command', '--skill-id', 'delivery-api',
            '--command', 'contract', '--', '--json'], check=True, capture_output=True, text=True)
        self.assertTrue(result.stdout.strip())
        owner = Path(protocol['owner_repository'])
        return req, values, protocol, owner

    def assert_resume_operation_prompt_projection(self, *, interrupted):
        import io
        from contextlib import redirect_stdout
        from unittest.mock import patch
        from adapters.eval import stage_result_chain as chain

        req, values, protocol, owner = self.interrupted_fixture()
        if not interrupted:
            # An ended adapter receipt selects normal continuation in this fixture.
            stage.write_json(Path(protocol['native_request_path']).parent / 'adapter-transcript.json',
                             {'returncode': 0})
        route = chain.INTERRUPTED_PROTOCOL_ENV if interrupted else chain.RESUME_PROTOCOL_ENV
        continued_request = request(Path(req['workdir']).parents[1] / 'prompt-continuation',
                                    'guru-review-task-completion', 'p04')
        continued_request['case_id'] = chain.CASE
        operation_prompt = (
            'Create each new transient file with exclusive creation.\n'
            'Preserve historical input files byte-for-byte.\n'
            'Reconstruct complete raw source, diff and actual command observations.\n'
            'An independent owner must freshly judge coverage before dependent review.\n'
            '必要原始事实保留来源与完整条件；不得提供判断答案或预期出口。\n'
        )
        continued_request['prompt'] = operation_prompt
        with patch.dict(os.environ, {route: str(values[4])}):
            continued = native_adapter.build_context(continued_request, 'codex')
        self.addCleanup(lambda: continued[8].join(timeout=2))
        self.addCleanup(continued[9].set)
        continued_protocol = json.loads(continued[4].read_text())
        self.assertEqual(continued_protocol['owner_repository'], str(owner))
        request_path = Path(continued_request['workdir']).parents[1] / 'request.json'
        stage.write_json(request_path, continued_request)
        authorities = ['docs/architecture/00-foundation/design-constitution.md',
                       'docs/architecture/README.md',
                       'docs/architecture/06-governance/change-contract.md']
        # Only dispatch/context is exercised; the fake worker invokes no semantic owner.
        reviewer_input = {'schema_version': 'delivery-3.0',
                          'profile': 'delivery_task_impact_sync', 'stage': 'branch_review',
                          'constitution': {'authority_locator': authorities[0]},
                          'baseline': {'locator': authorities[1]},
                          'project_contract': {'change_contract_locator': authorities[2]}}
        captured = {}
        original_run = subprocess.run

        def fake_native(argv, **kwargs):
            if len(argv) < 2 or argv[1] != 'exec':
                return original_run(argv, **kwargs)
            context_path = Path(kwargs['cwd']) / 'native-context.txt'
            output = Path(argv[argv.index('--output-last-message') + 1])
            kind = 'worker' if output.parent.name.startswith('architecture-worker-') else 'main'
            captured[kind] = {'argv': list(argv), 'context': context_path.read_bytes()}
            if kind == 'main':
                relay = continued[8].implementation_commands
                result = relay.independent_reviewer({'public_input': reviewer_input,
                                                     'reads': authorities})
                self.assertEqual(result['returncode'], 2)
                self.assertEqual(context_path.read_bytes(), captured['main']['context'])
            return subprocess.CompletedProcess(argv, 2, '', 'fake native context probe')

        output = io.StringIO()
        with patch.object(sys, 'argv', ['native_adapter', '--adapter', 'codex',
                '--native-command', sys.executable, '--request', str(request_path)]), \
             patch.object(native_adapter, 'build_context', return_value=continued), \
             patch.object(native_adapter, 'prepare_isolated_codex_permissions', return_value=(None, [])), \
             patch.object(native_adapter, 'run_codex_permission_probe', return_value={'returncode': 0}), \
             patch.object(native_adapter.subprocess, 'run', side_effect=fake_native), \
             redirect_stdout(output):
            native_adapter.main()
        self.assertEqual(json.loads(output.getvalue())['capability_status'], 'execution_error')
        self.assertEqual(set(captured), {'main', 'worker'})
        main_context = captured['main']['context']
        self.assertEqual(main_context.count(operation_prompt.encode()), 1)
        self.assertEqual(captured['main']['argv'][-1].encode(), main_context)
        self.assertEqual(continued[1].read_bytes(), main_context)
        self.assertEqual(json.loads(continued[5].read_text())['prompt'], operation_prompt)
        transcript = json.loads(request_path.with_name('adapter-transcript.json').read_text())
        self.assertEqual(transcript['argv'], captured['main']['argv'])
        worker_context = captured['worker']['context']
        self.assertEqual(captured['worker']['argv'][-1].encode(), worker_context)
        self.assertIn(b'fresh independent Architecture reviewer', worker_context)
        for instruction in operation_prompt.splitlines():
            self.assertNotIn(instruction.encode(), worker_context)

    def test_ended_resume_delivers_operation_prompt_and_isolates_architecture(self):
        self.assert_resume_operation_prompt_projection(interrupted=False)

    def test_interrupted_resume_delivers_operation_prompt_and_isolates_architecture(self):
        self.assert_resume_operation_prompt_projection(interrupted=True)

    def test_interrupted_inspection_is_read_only_and_resume_keeps_same_task(self):
        from adapters.eval import stage_result_chain as chain
        from unittest.mock import patch
        from adapters.eval.eval_support import repository_file_inventory
        req, values, protocol, owner = self.interrupted_fixture()
        facts = json.loads((owner / stage.FACTS).read_text())
        projection = DeliveryProjection(owner, facts['task_ref'])
        task_before = projection.read_record()
        delivery_before = projection.resolve(facts['delivery_key'])
        evidence = [values[4], Path(protocol['native_request_path']),
            Path(protocol['trace_path']), Path(protocol['implementation_receipts_path'])]
        originals = {path: path.read_bytes() for path in evidence}
        before = repository_file_inventory(owner)
        inspected = chain.inspect_interrupted_segment(req, values[4])
        self.assertEqual(repository_file_inventory(owner), before)
        self.assertEqual(inspected['owner_repository'], str(owner))
        self.assertEqual(inspected['delivery_key'], facts['delivery_key'])
        self.assertEqual(inspected['command_count'], 1)
        self.assertEqual(inspected['preceding_owner_command_count'], 1)
        continued_request = request(Path(req['workdir']).parents[1] / 'continued',
            'guru-review-task-completion', 'p04')
        continued_request['case_id'] = chain.CASE
        with patch.dict(os.environ, {chain.INTERRUPTED_PROTOCOL_ENV: str(values[4])}):
            continued = native_adapter.build_context(continued_request, 'codex')
        self.addCleanup(lambda: continued[8].join(timeout=2))
        self.addCleanup(continued[9].set)
        continued_protocol = json.loads(continued[4].read_text())
        self.assertEqual(continued_protocol['owner_repository'], str(owner))
        self.assertEqual(continued_protocol['implementation_context_id'], protocol['implementation_context_id'])
        resumed = json.loads((owner / stage.FACTS).read_text())
        continuation = json.loads((owner / resumed['continuation_locator']).read_text())
        after = repository_file_inventory(owner)
        changed = {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}
        self.assertEqual(changed, {stage.FACTS, resumed['continuation_locator']})
        receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
        self.assertEqual(continuation['preceding_commands'], [
            {name: row[name] for name in ('request', 'response')} for row in receipts])
        self.assertEqual(projection.read_record(), task_before)
        self.assertEqual(projection.resolve(facts['delivery_key']), delivery_before)
        self.assertTrue(all(result is None for result in delivery_before['results'].values()))
        self.assertIsNone(delivery_before['delivery_result'])
        self.assertEqual({path: path.read_bytes() for path in evidence}, originals)
        self.assertFalse((Path(protocol['native_request_path']).parent / 'adapter-transcript.json').exists())
        with patch.dict(os.environ, {chain.RESUME_PROTOCOL_ENV: str(values[4])}):
            with self.assertRaisesRegex(ValueError, 'ended actual native chain segment'):
                chain.resume_execution(req)

    def test_interrupted_route_blocks_ended_segment_and_stale_selection(self):
        from adapters.eval import stage_result_chain as chain
        req, values, protocol, owner = self.interrupted_fixture()
        with self.assertRaisesRegex(ValueError, 'protocol and native request differ'):
            chain.inspect_interrupted_segment({**req, 'case_id': 'native-stage-p04'}, values[4])
        transcript = Path(protocol['native_request_path']).parent / 'adapter-transcript.json'
        # A normal adapter return is an ended-segment fact in this isolated fixture.
        stage.write_json(transcript, {'returncode': 0})
        with self.assertRaisesRegex(ValueError, 'ended native result'):
            chain.inspect_interrupted_segment(req, values[4])
        transcript.unlink()
        facts = json.loads((owner / stage.FACTS).read_text())
        projection = DeliveryProjection(owner, facts['task_ref'])
        projection.release(facts['delivery_key'])
        with self.assertRaisesRegex(ValueError, 'same current Task and Delivery'):
            chain.inspect_interrupted_segment(req, values[4])

    def create_interrupted_successor(self, owner, facts, projection, context_id, prefix=None):
        record = projection.read_record()
        public = {'profile': 'delivery_creation', 'mode': 'workflow',
            'task_ref': facts['task_ref'],
            'task_key': {'task_id': record['id'], 'lifecycle_generation': record['lifecycle_generation']},
            'scope_ref': {'authority': record['accepted_scope'], 'anchors': ['R2. Implementation slice']},
            'delivery_profile': 'pull_request', 'continuation_id': 'interrupted-successor', 'action': 'create'}
        runtime = owner / '.trellis/.runtime/guru-team/evals'
        source, result = runtime / 'successor-input.json', runtime / 'successor-owner.json'
        stage.write_json(source, public)
        stage.write_json(result, {'typed_exit': 'created',
            'reason': 'Deterministic Creation/Selection probe; no native semantic review claim.'})
        arguments = ['--input', str(source), '--owner-result', str(result)]
        command = ([*prefix, 'command', '--skill-id', 'guru-create-delivery',
            '--command', 'invoke', '--'] if prefix else
            [str(owner / '.trellis/guru-team/skills/packages/guru-create-delivery/scripts/invoke.sh')])
        process = subprocess.run([*command, *arguments], cwd=owner, text=True, capture_output=True,
            env={**os.environ, 'TRELLIS_CONTEXT_ID': context_id})
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        created = json.loads(process.stdout)
        self.assertEqual(created['exit_id'], 'created', created)
        return created['delivery_key']

    def test_interrupted_resume_proves_delivery_progression_and_preserves_origin(self):
        from adapters.eval import stage_result_chain as chain
        from adapters.eval.eval_support import repository_file_inventory
        from unittest.mock import patch
        with self.merged_transport_fixture() as (req, values, protocol, owner, facts, projection, prefix):
            key = self.create_interrupted_successor(owner, facts, projection,
                protocol['implementation_context_id'], prefix)
            evidence = [values[4], Path(protocol['native_request_path']),
                Path(protocol['trace_path']), Path(protocol['implementation_receipts_path']), owner / stage.FACTS]
            originals = {p: p.read_bytes() for p in evidence}
            before = repository_file_inventory(owner)
            inspected = chain.inspect_interrupted_segment(req, values[4])
            self.assertEqual(inspected['delivery_key'], key)
            self.assertEqual(inspected['planning_root'], projection.resolve(key)['planning_root'])
            self.assertEqual(repository_file_inventory(owner), before)
            self.assertEqual({p: p.read_bytes() for p in evidence}, originals)
            for stale_key in ({**key, 'task_id': 'another-task'},
                              {**key, 'lifecycle_generation': key['lifecycle_generation'] + 1}):
                with self.subTest(stale_key=stale_key), patch.object(DeliveryProjection, 'current',
                        return_value={'kind': 'current', 'key': stale_key}):
                    with self.assertRaisesRegex(ValueError, 'same current Task and Delivery'):
                        chain.inspect_interrupted_segment(req, values[4])
            continued_request = request(Path(req['workdir']).parents[1] / 'continued',
                'guru-review-task-completion', 'p04')
            continued_request['case_id'] = chain.CASE
            with patch.dict(os.environ, {chain.INTERRUPTED_PROTOCOL_ENV: str(values[4])}):
                continued = native_adapter.build_context(continued_request, 'codex')
            self.addCleanup(lambda: continued[8].join(timeout=2))
            self.addCleanup(continued[9].set)
            self.assertEqual(json.loads((owner / stage.FACTS).read_text())['delivery_key'], facts['delivery_key'])
            current_protocol = json.loads(continued[4].read_text())
            read = shlex.split(continued[0].splitlines()[1])
            subprocess.run(read, check=True, capture_output=True)
            current_prefix = read[:read.index('read')]
            subprocess.run([*current_prefix, 'command', '--skill-id', 'delivery-api',
                '--command', 'contract', '--', '--json'], check=True, capture_output=True)
            current_rows = json.loads(Path(current_protocol['implementation_receipts_path']).read_text())
            self.assertEqual(len(current_rows), 1)
            current_before = repository_file_inventory(owner)
            resumed = chain.inspect_interrupted_segment(continued_request, continued[4])
            self.assertEqual(resumed['delivery_key'], key)
            self.assertEqual(repository_file_inventory(owner), current_before)
            self.assertEqual(projection.read_record()['completion_results'], [])

    def test_interrupted_progression_requires_delivery_and_recorded_creation(self):
        from adapters.eval import stage_result_chain as chain
        from unittest.mock import patch
        req, values, protocol, owner = self.interrupted_fixture()
        facts = json.loads((owner / stage.FACTS).read_text())
        projection = DeliveryProjection(owner, facts['task_ref'])
        with patch.dict(os.environ, {'TRELLIS_CONTEXT_ID': protocol['implementation_context_id']}):
            projection.release(facts['delivery_key'])
        read = shlex.split(values[0].splitlines()[1])
        self.create_interrupted_successor(owner, facts, projection,
            protocol['implementation_context_id'], read[:read.index('read')])
        self.assertNotEqual(projection.resolve(facts['delivery_key'])['phase'], 'delivered')
        with self.assertRaisesRegex(ValueError, 'same current Task and Delivery'):
            chain.inspect_interrupted_segment(req, values[4])
        for missing in ('creation', 'merge'):
            with self.subTest(missing_receipt=missing), self.merged_transport_fixture(
                    record_merge=missing != 'merge') as (req, values, protocol, owner, facts, projection, prefix):
                # Both original owners execute. One call has no helper receipt,
                # so live state alone cannot fill this ordinary output loss.
                self.create_interrupted_successor(owner, facts, projection,
                    protocol['implementation_context_id'], prefix if missing == 'merge' else None)
                with self.assertRaisesRegex(ValueError, 'same current Task and Delivery'):
                    chain.inspect_interrupted_segment(req, values[4])

    def test_chain_continuation_routes_conflict_before_staging(self):
        from adapters.eval import stage_result_chain as chain
        from unittest.mock import patch
        with patch.dict(os.environ, {chain.RESUME_PROTOCOL_ENV: 'ended.json',
                chain.INTERRUPTED_PROTOCOL_ENV: 'partial.json'}):
            with self.assertRaisesRegex(ValueError, 'conflicting chain continuation invocation'):
                native_adapter.build_context({'case_id': chain.CASE}, 'codex')

    def failed_transport_fixture(self):
        """Reproduce the old carrier configuration and its real stash/recorder failure."""
        from adapters.eval import stage_result_chain as chain
        from unittest.mock import patch
        req, values, _, owner = self.interrupted_fixture()
        continued = request(Path(req['workdir']).parents[1] / 'transport-segment',
            'guru-review-task-completion', 'p04')
        continued['case_id'] = chain.CASE
        with patch.dict(os.environ, {chain.INTERRUPTED_PROTOCOL_ENV: str(values[4])}):
            next_values = native_adapter.build_context(continued, 'codex')
        self.addCleanup(lambda: next_values[8].join(timeout=2))
        self.addCleanup(next_values[9].set)
        protocol = json.loads(next_values[4].read_text())
        # The affected existing fixture predates the new carrier exclusions.
        exclude = Path(subprocess.check_output(
            ['git', 'rev-parse', '--git-path', 'info/exclude'], cwd=owner, text=True).strip())
        excluded = {'/' + path for path in chain.CARRIER_PATHS}
        exclude.write_text('\n'.join(line for line in exclude.read_text().splitlines()
                                    if line not in excluded) + '\n')
        read = shlex.split(next_values[0].splitlines()[1])
        prefix = read[:read.index('read')]
        inspected = subprocess.run([*prefix, 'command', '--skill-id', 'implementation-authoring',
            '--command', 'inspect'], input='', text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(inspected.stdout)['head'],
                         subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=owner, text=True).strip())
        failed = subprocess.run([*prefix, 'command', '--skill-id', 'implementation-authoring',
            '--command', 'run', '--stdin'], input=json.dumps({'argv': ['git', 'stash', 'push',
                '--include-untracked', '-m', 'carrier transport probe', '--',
                '.trellis/tasks/stage-result-evidence']}), text=True, capture_output=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('facts.json', failed.stderr)
        self.assertFalse((owner / stage.FACTS).exists())
        projected = Path(protocol['repository_projection_root'])
        for path in chain.CARRIER_PATHS:
            target = owner / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(projected / path, target)
        # Save the actual helper error as this unit fixture's terminal message.
        # This is a transport probe, not a native Agent or semantic pass.
        last = Path(protocol['model_root']) / 'output/native-last-message.txt'
        last.parent.mkdir(parents=True, exist_ok=True)
        last.write_text(failed.stderr)
        next_values[9].set(); next_values[8].join(timeout=2)
        return continued, next_values, protocol, owner, failed.stderr

    def test_failed_transport_reads_live_side_effects_and_resumes_without_filling_history(self):
        from adapters.eval import stage_result_chain as chain
        from adapters.eval.eval_support import repository_file_inventory
        from unittest.mock import patch
        req, values, protocol, owner, actual_error = self.failed_transport_fixture()
        facts = json.loads((owner / stage.FACTS).read_text())
        projection = DeliveryProjection(owner, facts['task_ref'])
        task = projection.read_record()
        before = repository_file_inventory(owner)
        originals = {path: Path(path).read_bytes() for path in (
            protocol['trace_path'], protocol['implementation_receipts_path'], protocol['native_request_path'])}
        inspected = chain.inspect_resume_segment(req, values[4])
        self.assertEqual(repository_file_inventory(owner), before)
        self.assertIn('refs/stash', inspected['live']['refs'])
        self.assertEqual(inspected['native_error'], actual_error.strip())
        self.assertEqual(projection.read_record(), task)
        commands = json.loads(Path(protocol['trace_path']).read_text())['events']
        receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
        self.assertEqual(len([row for row in commands if row['kind'] == 'command']), len(receipts) + 1)
        following = request(Path(req['workdir']).parents[1] / 'following',
                            'guru-review-task-completion', 'p04')
        following['case_id'] = chain.CASE
        with patch.dict(os.environ, {chain.RESUME_PROTOCOL_ENV: str(values[4])}):
            resumed = native_adapter.build_context(following, 'codex')
        self.addCleanup(lambda: resumed[8].join(timeout=2))
        self.addCleanup(resumed[9].set)
        self.assertEqual(json.loads(resumed[4].read_text())['owner_repository'], str(owner))
        self.assertIn(actual_error.strip(), resumed[0])
        self.assertIn('refs/stash', resumed[0])
        self.assertEqual(projection.read_record(), task)
        self.assertEqual({path: Path(path).read_bytes() for path in originals}, originals)
        self.assertFalse((Path(protocol['native_request_path']).parent / 'adapter-transcript.json').exists())
        self.assertTrue(all(value is None for value in task['deliveries'][0]['results'].values()))

    def test_failed_transport_keeps_original_routes_and_rejects_changed_runtime_or_head(self):
        from adapters.eval import stage_result_chain as chain
        req, values, protocol, owner, _ = self.failed_transport_fixture()
        with self.assertRaisesRegex(ValueError, 'ended native result'):
            chain.inspect_interrupted_segment(req, values[4])
        runtime_file = owner / '.trellis/guru-team/runtime/requirements.lock'
        original = runtime_file.read_bytes()
        runtime_file.write_bytes(original + b'\n# Different installed runtime candidate\n')
        with self.assertRaisesRegex(ValueError, 'shared runtime differs'):
            chain.inspect_resume_segment(req, values[4])
        runtime_file.write_bytes(original)
        (owner / 'docs/ordinary-followup.md').write_text('A later real commit changes this candidate.\n')
        subprocess.run(['git', 'add', 'docs/ordinary-followup.md'], cwd=owner, check=True)
        subprocess.run(['git', 'commit', '-qm', 'later fixture candidate'], cwd=owner, check=True)
        with self.assertRaisesRegex(ValueError, 'owner state changed'):
            chain.inspect_resume_segment(req, values[4])

    @contextmanager
    def merged_transport_fixture(self, *, record_merge=True):
        import hashlib
        import importlib.util
        from unittest.mock import patch
        from adapters.eval import stage_result_chain as chain

        with tempfile.TemporaryDirectory() as temporary:
            req = request(Path(temporary), 'guru-review-task-completion', 'p04')
            req['case_id'] = chain.CASE
            values = native_adapter.build_context(req, 'codex')
            try:
                protocol = json.loads(values[4].read_text())
                owner = Path(protocol['owner_repository'])
                facts = json.loads((owner / stage.FACTS).read_text())
                read = shlex.split(values[0].splitlines()[1])
                subprocess.run(read, check=True, capture_output=True)
                prefix = read[:read.index('read')]
                subprocess.run([*prefix, 'command', '--skill-id', 'delivery-api',
                    '--command', 'contract', '--', '--json'], check=True, capture_output=True)
                projection = DeliveryProjection(owner, facts['task_ref'])
                key = facts['delivery_key']

                def git(*argv):
                    return subprocess.check_output(['git', *argv], cwd=owner, text=True).strip()

                base = git('rev-parse', 'HEAD')
                (owner / 'contract.txt').write_text('Actual merged provider artifact.\n')
                git('add', 'contract.txt')
                git('commit', '-qm', 'transport regression')
                head = git('rev-parse', 'HEAD')
                git('push', 'origin', 'HEAD:refs/heads/merge-retirement')
                environment = patch.dict(os.environ, {
                    'PATH': facts['provider_bin'] + os.pathsep + os.environ['PATH']})
                environment.start()
                self.addCleanup(environment.stop)
                gh = Path(facts['provider_bin']) / 'gh'
                body = 'Refs #1. Test-provider artifact only.'
                subprocess.run([str(gh), 'pr', 'create', '--head', 'merge-retirement',
                    '--base', 'main', '--title', 'transport regression', '--body', body],
                    cwd=owner, check=True, capture_output=True)
                candidate = projection.candidate(['contract.txt'], head_ref=head, base_ref=base)
                record = projection.read_record()
                publication_id = 'publication:transport-entry'
                # The original public store seeds only the terminal-read entry.
                # The provider performs a real Git merge; no native gate is claimed.
                projection.apply({'api_version': '1.0', 'operation': 'record_publication',
                    'key': key, 'owner_role': 'publication',
                    'owner_id': projection.declaration()['owners']['publication'],
                    'expected_phase': 'planning', 'historical_success': True,
                    'result': {'result_id': publication_id,
                        'owner_id': projection.declaration()['owners']['publication'],
                        'evidence': [record['accepted_scope']], 'profile': 'pull_request',
                        'candidate': candidate, 'repo_ref': 'example/stage-chain',
                        'pr_number': 1, 'reviewed_head': head, 'target_ref': 'main',
                        'publication_ref': {'locator': 'https://github.com/example/stage-chain/pull/1',
                            'revision': 'sha256:' + hashlib.sha256(body.encode()).hexdigest()}}})
                package = owner / '.trellis/guru-team/skills/packages/guru-merge-task-delivery'
                spec = importlib.util.spec_from_file_location(
                    'stage_merge_transport_owner', package / 'runtime/owner.py')
                merge_owner = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(merge_owner)
                subject = 'chore(merge): 测试运输输入退休'
                message = '真实本地 Git 合并；只证明测试运输。\n\n' + '\n'.join(
                    merge_owner.expected_trailers(key['task_id'], head, key))
                runtime = owner / '.trellis/.runtime/guru-team/evals'
                message_file = runtime / 'merge-body.txt'
                message_file.write_text(message)
                subprocess.run([str(gh), 'pr', 'merge', '1', '--merge',
                    '--match-head-commit', head, '--subject', subject,
                    '--body-file', str(message_file)], cwd=owner, check=True, capture_output=True)
                public = {'profile': 'delivery_ready_for_merge', 'mode': 'workflow',
                    'task_ref': facts['task_ref'], 'delivery_key': key,
                    'publication_result_id': publication_id, 'repo_ref': 'example/stage-chain',
                    'pr_number': 1, 'expected_head_sha': head,
                    'publication_body_sha256': hashlib.sha256(body.encode()).hexdigest()}
                review = {'dimensions': [{'id': name, 'status': 'passed',
                    'summary': 'Deterministic transport probe; no native review claim.'}
                    for name in merge_owner.DIMENSIONS], 'route': {'typed_exit': 'delivered',
                    'merge_method': 'merge', 'merge_message': {'subject': subject, 'body': message}}}
                input_file = runtime / 'merge-input.json'
                review_file = runtime / 'merge-review.json'
                unconsumed = runtime / 'unused-input.json'
                input_file.write_text(json.dumps(public))
                review_file.write_text(json.dumps(review))
                unconsumed.write_text('{}')
                command = ([*prefix, 'command', '--skill-id', 'guru-merge-task-delivery',
                    '--command', 'invoke', '--'] if record_merge else
                    [str(package / 'scripts/invoke.sh')])
                process = subprocess.run([*command,
                    '--input', str(input_file), '--review-input', str(review_file)],
                    cwd=owner, text=True, capture_output=True,
                    env={**os.environ, 'TRELLIS_CONTEXT_ID': protocol['implementation_context_id']})
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                self.assertEqual(json.loads(process.stdout)['exit_id'], 'delivered')
                self.assertEqual(input_file.exists(), not record_merge)
                self.assertEqual(review_file.exists(), not record_merge)
                self.assertTrue(unconsumed.exists())
                yield req, values, protocol, owner, facts, projection, prefix
            finally:
                values[9].set()
                values[8].join(timeout=2)

    def test_original_merge_retires_consumed_review_input(self):
        with self.merged_transport_fixture():
            pass

    def test_run_input_errors_leave_transport_available_for_corrected_command(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            facts = root / stage.FACTS
            facts.parent.mkdir(parents=True)
            facts.write_text(json.dumps({'writable_paths': []}))
            relay = stage.ImplementationCommands(root, dict(os.environ), root / 'receipts.json',
                                                facts_relative=stage.FACTS)
            for supplied in ('', '{', '{}', '{"argv":[]}'):
                with self.subTest(stdin=supplied):
                    failed = relay.forward({'skill_id': 'implementation-authoring', 'command': 'run',
                        'arguments': [], 'stdin': supplied})
                    self.assertEqual(failed['returncode'], 0)
                    self.assertEqual(json.loads(failed['stdout'])['returncode'], 2)
                    self.assertFalse(relay.terminal)
            for supplied in ('', '{', '{}'):
                failed = relay.forward({'skill_id': 'implementation-authoring', 'command': 'write',
                    'arguments': [], 'stdin': supplied})
                self.assertEqual(failed['returncode'], 0)
                self.assertEqual(json.loads(failed['stdout'])['returncode'], 2)
                self.assertFalse(relay.terminal)
            corrected = relay.forward({'skill_id': 'implementation-authoring', 'command': 'run',
                'arguments': [], 'stdin': json.dumps({'argv': [sys.executable, '-c', 'print(42)']})})
            self.assertEqual(json.loads(corrected['stdout'])['stdout'], '42\n')

    def test_missing_run_executable_is_an_inner_failure_and_transport_continues(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            facts = root / stage.FACTS
            facts.parent.mkdir(parents=True)
            facts.write_text(json.dumps({'writable_paths': []}))
            relay = stage.ImplementationCommands(root, dict(os.environ), root / 'receipts.json',
                                                facts_relative=stage.FACTS)
            failed = relay.forward({'skill_id': 'implementation-authoring', 'command': 'run',
                'arguments': [], 'stdin': json.dumps({'argv': [str(root / 'missing-python')]})})
            self.assertEqual(failed['returncode'], 0)
            self.assertEqual(json.loads(failed['stdout'])['returncode'], 127)
            self.assertFalse(relay.terminal)
            recovered = relay.forward({'skill_id': 'implementation-authoring', 'command': 'run',
                'arguments': [], 'stdin': json.dumps({'argv': [sys.executable, '-c', 'print(42)']})})
            self.assertEqual(json.loads(recovered['stdout'])['stdout'], '42\n')

    def test_check_fixtures_execute_real_green_tests_and_expose_actual_consumer(self):
        for case in ('c01', 'c02', 'c03', 'c04'):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                req = request(Path(temporary), 'guru-check-task', case)
                values = native_adapter.build_context(req, 'codex')
                try:
                    protocol = json.loads(values[4].read_text())
                    owner = Path(protocol['owner_repository'])
                    from runtime.reviewed_content import reviewed_content_identity
                    from adapters.eval import phase2_authoring
                    architecture = json.loads((owner / phase2_authoring.ARCHITECTURE_INPUT).read_text())
                    self.assertEqual(architecture['candidate']['content_identity'],
                                     'sha256:' + reviewed_content_identity(owner)['sha256'])
                    tests = json.loads((owner / 'docs/phase2-evidence/validation.json').read_text())
                    self.assertEqual(tests['returncode'], 0, tests['stderr'])
                    consumer = json.loads((owner / 'docs/phase2-evidence/consumer-observation.json').read_text())
                    facts = json.loads((owner / phase2_authoring.FACTS).read_text())
                    self.assertIn('docs/phase2-evidence/consumer-observation.json', facts['reviewed_paths'])
                    self.assertEqual(consumer['additional_probes']['returncode'] == 0, case != 'c03')
                    if case == 'c03':
                        self.assertNotEqual(consumer['returncode'], 0)
                        self.assertIn('NotImplementedError', consumer['stderr'])
                    else:
                        self.assertEqual(consumer['returncode'], 0, consumer['stderr'])
                        self.assertEqual(json.loads(consumer['stdout']), [2, 3, 4])
                    public = json.loads((owner / 'docs/phase2-evidence/check-public-input.json').read_text())
                    delivery = DeliveryProjection(owner, public['task_ref']).resolve(public['delivery_key'])
                    if case == 'c03':
                        before_consumer = subprocess.check_output(['git', 'show',
                            delivery['candidate']['base_ref'] + ':range_filter.py'], cwd=owner)
                        self.assertEqual(before_consumer, (owner / 'range_filter.py').read_bytes())
                    self.assertTrue(set(delivery['candidate']['paths']).issubset(facts['reviewed_paths']))
                    self.assertFalse(any(path.startswith('.trellis/guru-team/')
                                         for path in delivery['candidate']['paths']))
                    self.assertEqual(delivery['phase'], 'checking')
                    self.assertIsNone(delivery['results']['check'])
                finally:
                    values[9].set(); values[8].join(timeout=2)

    def test_completion_staging_uses_original_delivery_fact_and_current_task_key(self):
        with tempfile.TemporaryDirectory() as temporary:
            req = request(Path(temporary), 'guru-review-task-completion', 'p02')
            values = native_adapter.build_context(req, 'codex')
            try:
                protocol = json.loads(values[4].read_text())
                owner = Path(protocol['owner_repository'])
                facts = json.loads((owner / stage.FACTS).read_text())
                projection = DeliveryProjection(owner, facts['task_ref'])
                record = projection.read_record()
                self.assertEqual(record['completion_results'], [])
                scope = (owner / facts['task_ref'] / 'prd.md').read_text()
                self.assertIn('requires consumer.consume(values)', scope)
                self.assertIn('requires no Control receipt', scope)
                observed = json.loads((owner / 'docs/consumer-observation.json').read_text())
                self.assertEqual(observed['returncode'], 1)
                self.assertIn('Control receipt required', observed['stderr'])
                delivery = projection.resolve(facts['delivery_key'])
                self.assertEqual(delivery['phase'], 'delivered')
                self.assertEqual(delivery['delivery_result']['profile'], 'pull_request')
                self.assertEqual(delivery['delivery_result']['candidate']['head_ref'],
                                 delivery['delivery_result']['reviewed_head'])
                from runtime.reviewed_content import reviewed_content_identity
                prerequisite = json.loads((owner / stage.ARCHITECTURE_PREREQUISITE).read_text())
                identity = 'sha256:' + reviewed_content_identity(owner)['sha256']
                self.assertEqual(prerequisite['public_input']['candidate']['content_identity'], identity)
                (owner / stage.REASONING).write_text('# Actual current owner explanation\n')
                self.assertEqual('sha256:' + reviewed_content_identity(owner)['sha256'], identity)
                original = owner / '.trellis/guru-team/skills/packages/guru-review-task-completion/scripts/invoke.sh'
                public = json.loads((owner / stage.PUBLIC_INPUT).read_text())
                from adapters.eval.fixture_io import public_input_path
                self.assertEqual(json.loads(public_input_path(req).read_text()), public)
                semantic = {'profile': 'delivery_completion', 'mode': 'workflow',
                    'reviewed_task_key': public['task_key'], 'reviewed_scope': record['accepted_scope'],
                    'reviewed_delivery_result_ids': [delivery['delivery_result']['result_id']],
                    'evidence': [record['accepted_scope']], 'remaining_work_refs': [],
                    'result_id': 'completion:deterministic-transport-only', 'route': {'typed_exit': 'completed'}}
                transient = owner / '.trellis/.runtime/guru-team/evals/transport-semantic.json'
                transient.write_text(json.dumps(semantic))
                relay = stage.ImplementationCommands(owner,
                    {**os.environ, 'TRELLIS_CONTEXT_ID': protocol['implementation_context_id']},
                    Path(temporary) / 'receipts.json', facts_relative=stage.FACTS)
                facts_before = (owner / stage.FACTS).read_bytes()
                result = relay.forward({'skill_id': 'guru-review-task-completion',
                    'command': 'invoke-guru-review-task-completion',
                    'arguments': ['--root', str(owner), '--input', stage.PUBLIC_INPUT,
                                  '--semantic-result', str(transient)],
                    'stdin': json.dumps({'final': True, 'invocation': {}})})
                self.assertEqual(result['returncode'], 0, result['stderr'] or result['stdout'])
                self.assertEqual(json.loads(result['stdout'])['exit_id'], 'completed')
                self.assertTrue(relay.terminal)
                self.assertFalse(transient.exists())
                self.assertIn(transient.relative_to(owner).as_posix(), relay.consumed_paths)
                self.assertEqual((owner / stage.FACTS).read_bytes(), facts_before)
                self.assertTrue((owner / stage.PUBLIC_INPUT).is_file())
                self.assertEqual(len(projection.read_record()['completion_results']), 1)
            finally:
                values[9].set(); values[8].join(timeout=2)

    def test_delivery_review_transport_reaches_original_schema_without_host_result(self):
        with tempfile.TemporaryDirectory() as temporary:
            req = request(Path(temporary), 'guru-review-task-delivery', 'd01')
            values = native_adapter.build_context(req, 'codex')
            try:
                protocol = json.loads(values[4].read_text())
                owner = Path(protocol['owner_repository'])
                facts = json.loads((owner / stage.FACTS).read_text())
                projection = DeliveryProjection(owner, facts['task_ref'])
                self.assertIsNone(projection.resolve(facts['delivery_key'])['results']['readiness'])
                semantic = owner / '.trellis/.runtime/guru-team/evals/missing-semantic.json'
                semantic.write_text('{}')
                relay = stage.ImplementationCommands(owner,
                    {**os.environ, 'TRELLIS_CONTEXT_ID': protocol['implementation_context_id']},
                    Path(temporary) / 'receipts.json', facts_relative=stage.FACTS)
                result = relay.forward({'skill_id': 'guru-review-task-delivery', 'command': 'invoke',
                    'arguments': ['--root', str(owner), '--input', stage.PUBLIC_INPUT,
                                  '--semantic-result', str(semantic)], 'stdin': ''})
                self.assertNotEqual(result['returncode'], 0)
                self.assertIn('schema_mismatch', result['stdout'] + result['stderr'])
                self.assertTrue(relay.terminal)
                self.assertIsNone(projection.resolve(facts['delivery_key'])['results']['readiness'])
            finally:
                values[9].set(); values[8].join(timeout=2)


if __name__ == '__main__':
    unittest.main()
