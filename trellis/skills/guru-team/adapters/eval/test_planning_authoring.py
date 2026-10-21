"""Objective Author file/identity transport; native behavior is graded separately."""
from __future__ import annotations
import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import native_adapter, owner_staging, planning_authoring
from runtime.schema import validate_json
from runtime.delivery_projection.adapter import DeliveryProjection
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.task_lifecycle.git_facts import branch_checked_out_paths
from runtime.task_lifecycle.resource_ledger import ResourceLedgerStore
from adapters.eval.fixture_io import run_git
SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
PACKAGE = SKILLS / 'packages/guru-author-task-plan'


def request(root):
    case = json.loads((PACKAGE / 'evals/evals.json').read_text())['evals'][0]
    work = root / 'execution/workdir'
    work.mkdir(parents=True)
    for path in case['files']:
        target = work / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PACKAGE / path, target)
    interface = json.loads((PACKAGE / 'interface.json').read_text())
    return {**{k:case[k] for k in ('prompt','files','model_id','native_execution_mode','native_execution_adapter')},
        'schema_version':'1.0','skill_id':PACKAGE.name,'case_id':case['id'],'package_root':str(PACKAGE),
        'workdir':str(work),'runtime_target':str(REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh'),
        'interface':{'public_invocation':interface['public_contracts']['invocation']}}


class PlanningAuthoringTests(unittest.TestCase):
    def test_native_context_preserves_real_upstream_and_unwritten_bodies(self):
        with tempfile.TemporaryDirectory() as temp:
            req = request(Path(temp))
            values = native_adapter.build_context(req, 'codex')
            try:
                context = values[0]
                protocol = json.loads(values[4].read_text())
                repo = Path(protocol['owner_repository'])
                facts = json.loads((repo / planning_authoring.FACTS).read_text())
                model_repo = Path(protocol['repository_projection_root'])
                projected = json.loads((model_repo / planning_authoring.FACTS).read_text())
                self.assertFalse((model_repo / '.git').exists())
                self.assertTrue((repo / '.git').is_file())
                repository = inspect_repository(repo)
                key = TaskLifecycleKey('current', 0)
                binding = BranchBindingStore(repository).read(key)
                resources = ResourceLedgerStore(repository).read_current(key)
                self.assertEqual((resources.binding_revision, resources.branch_name),
                                 (binding.binding_revision, binding.branch_name))
                self.assertNotEqual(binding.branch_name, 'main')
                self.assertEqual(branch_checked_out_paths(repository, binding.branch_ref), (repo,))
                self.assertEqual(projected['task_checkout']['branch_name'], resources.branch_name)
                self.assertEqual(projected['task_checkout']['binding_revision'], resources.binding_revision)
                public = json.loads((repo / planning_authoring.PUBLIC_INPUT).read_text())
                projection = DeliveryProjection(repo, public['task_ref'])
                actual_head = run_git(repo, 'rev-parse', 'HEAD')
                actual_target = run_git(repo, 'rev-parse', 'origin/main')
                actual_base = projection.content_base(public['delivery_key'],
                    development_base=actual_head, observed_target=actual_target)
                range_facts = projected['delivery_range']
                self.assertEqual(range_facts['delivery_key'], public['delivery_key'])
                self.assertEqual(range_facts['head'], actual_head)
                self.assertEqual(range_facts['development_base'], actual_head)
                self.assertEqual(range_facts['observed_target'], actual_target)
                self.assertEqual(range_facts['content_base'], actual_base)
                run_git(repo, 'cat-file', '-e', range_facts['content_base'] + '^{commit}')
                contract_path = range_facts['contract_locator'].split('#', 1)[0]
                self.assertTrue((model_repo / contract_path).is_file())
                self.assertFalse((model_repo / facts['planning_root'] / 'design.md').exists())
                self.assertNotIn('owner_result', projected)
                self.assertNotIn('typed_exit', projected)
                for path in facts['required_reads']:
                    self.assertTrue((repo / path).is_file(), path)
                self.assertTrue(protocol['architecture_context'])
                self.assertIn('--upstream-architecture', protocol['architecture_context'])
                def helper_reads(text):
                    commands = []
                    for line in text.splitlines():
                        first = line.split(maxsplit=1)
                        if not first or not first[0].endswith('native-trace-helper.py'):
                            continue
                        if ' read --kind ' not in line:
                            continue
                        arguments = shlex.split(line)
                        if arguments[0].endswith('native-trace-helper.py'):
                            commands.append(arguments)
                    return commands
                author_reads = helper_reads(context)
                author_skill = str(Path(protocol['projection_root']) / 'SKILL.md')
                author_skill_reads = [command for command in author_reads
                    if command[command.index('--path') + 1] == author_skill]
                self.assertEqual(len(author_skill_reads), 1)
                self.assertEqual(author_reads[0], author_skill_reads[0])
                architecture_reads = helper_reads(protocol['architecture_context'])
                self.assertTrue(architecture_reads)
                self.assertNotEqual(architecture_reads[0][architecture_reads[0].index('--path') + 1], author_skill)
                self.assertFalse(any(command[command.index('--path') + 1] == author_skill
                                     for command in architecture_reads))
                self.assertIn('file_updates', context)
                for path in facts['writable_paths']:
                    self.assertFalse((repo / path).exists(), path)
                architecture = json.loads((repo / planning_authoring.ARCHITECTURE_INPUT).read_text())
                validate_json(architecture, PACKAGE.parent / 'guru-maintain-architecture-baseline/schemas/public-input-delivery-task-impact-sync-1.0.schema.json', 'input')
                # Objective wrapper identity fixture only; no native semantic
                # approval is staged for or supplied to the evaluated Agent.
                owner = {name: architecture[name] for name in (
                    'schema_version', 'profile', 'mode', 'continuation_id', 'stage', 'task_locator',
                    'baseline', 'constitution', 'project_contract', 'freshness_identity',
                    'planning_purpose', 'delivery_key', 'planning_root')}
                owner.update(input_sha256=facts['architecture_input_sha256'], typed_exit='baseline_current',
                    baseline_identity=architecture['baseline']['identity'],
                    constitution_identity=architecture['constitution']['identity'],
                    impact_kind='no_architecture_impact', impact_reason='Objective identity transport fixture only.',
                    consumer={'kind':'workflow','id':'guru-architecture-baseline-current-router'},
                    ai_review_gate={'status':'passed','reviewed_scope':'Objective wrapper identity fixture',
                        'evidence_summary':'No native semantic review is claimed.', 'findings':[],
                        'conclusion':'Only original wrapper binding is checked.'})
                wrapper=repo/'.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline/scripts/invoke.sh'
                result=subprocess.run([str(wrapper),'--invocation','-'],cwd=repo,
                    input=json.dumps({'public_input':architecture,'owner_result':owner}),
                    env={**os.environ,'TRELLIS_CONTEXT_ID':os.environ.get('TRELLIS_CONTEXT_ID') or 'architecture-delivery-eval'},
                    capture_output=True,text=True,check=False)
                self.assertEqual(result.returncode,0,result.stderr)
                self.assertEqual(json.loads(result.stdout)['exit_id'],'baseline_current')
                self.assertNotIn('architecture_assessment', json.loads((repo / planning_authoring.PUBLIC_INPUT).read_text()))
                architecture_output = json.loads(result.stdout)
                author_public = {**public, 'architecture_assessment': {
                    name: architecture_output[name] for name in (
                        'planning_purpose', 'baseline_identity', 'constitution_identity',
                        'impact_kind', 'impact_reason')}}
                author_owner = {'public_input': author_public,
                    'output': {'exit_id': 'plan_ready', 'task_ref': public['task_ref'],
                               'delivery_key': public['delivery_key']},
                    'ai_review_gate': {'status': 'passed',
                        'summary': 'Objective identity and file transport test only; no native semantic approval is claimed.'}}
                updates = {path: ('' if path.endswith('.jsonl') else
                    '# Objective file transport fixture\n\nNative semantic review is evaluated separately.\n')
                    for path in facts['writable_paths']}
                selections = {
                    'implement': [
                        {'file': 'docs/source.md', 'reason': 'Read the complete source conditions.'},
                        {'file': 'docs/architecture/README.md', 'reason': 'Read actual module responsibilities.'},
                    ],
                    'check': [{'file': 'docs/source.md', 'reason': 'Compare behavior with the current source.'}],
                }
                for kind, entries in selections.items():
                    updates[f"{facts['planning_root']}/{kind}.jsonl"] = ''.join(
                        json.dumps(entry, ensure_ascii=False) + '\n' for entry in entries)
                environment = {**os.environ, 'TRELLIS_CONTEXT_ID':
                    os.environ.get('TRELLIS_CONTEXT_ID') or 'architecture-delivery-eval'}
                author_package = repo / '.trellis/guru-team/skills/packages/guru-author-task-plan'
                authored = planning_authoring.execute(
                    author_package, repo,
                    {'public_input': author_public, 'owner_result': author_owner, 'file_updates': updates},
                    environment)
                self.assertEqual(authored.returncode, 0, authored.stderr)
                self.assertEqual(json.loads(authored.stdout), author_owner['output'])
                receipts_path = repo.parent / 'planning-command-receipts.json'
                receipts = json.loads(receipts_path.read_text())
                self.assertEqual(len(receipts), 4)
                index = 0
                for kind, entries in selections.items():
                    actual = repo / facts['planning_root'] / (kind + '.jsonl')
                    self.assertEqual([json.loads(line) for line in actual.read_text().splitlines()], entries)
                    for entry in entries:
                        receipt = receipts[index]
                        index += 1
                        self.assertEqual(receipt['argv'], [sys.executable, '-B',
                            str(repo / '.trellis/scripts/task.py'), 'add-context', public['task_ref'],
                            kind, entry['file'], entry['reason'], '--delivery',
                            public['delivery_key']['delivery_id']])
                        self.assertEqual(receipt['returncode'], 0, receipt['stderr'])
                        self.assertIn('Added file:', receipt['stdout'])
                self.assertEqual(receipts[-1]['argv'][0], str(author_package / 'scripts/invoke.sh'))
                self.assertEqual(json.loads(receipts[-1]['stdout']), author_owner['output'])
                for path, content in updates.items():
                    if path.endswith('.md'):
                        self.assertEqual((repo / path).read_text(), content)

                empty_updates = {f"{facts['planning_root']}/{kind}.jsonl": '' for kind in selections}
                empty = planning_authoring.execute(author_package, repo,
                    {'public_input': author_public, 'owner_result': author_owner,
                     'file_updates': empty_updates}, environment)
                self.assertEqual(empty.returncode, 0, empty.stderr)
                self.assertEqual(json.loads(empty.stdout), author_owner['output'])
                self.assertEqual(len(json.loads(receipts_path.read_text())), 1)
                for path in empty_updates:
                    self.assertTrue((repo / path).is_file())
                    self.assertEqual((repo / path).read_bytes(), b'')

                missing_entry = {'file': 'docs/absent-context.md', 'reason': 'Author-selected missing input.'}
                failed = planning_authoring.execute(author_package, repo,
                    {'public_input': author_public, 'owner_result': author_owner,
                     'file_updates': {f"{facts['planning_root']}/implement.jsonl":
                                      json.dumps(missing_entry) + '\n'}}, environment)
                self.assertNotEqual(failed.returncode, 0)
                self.assertIn('Path not found: docs/absent-context.md', failed.stdout)
                receipts = json.loads(receipts_path.read_text())
                self.assertEqual(len(receipts), 1)
                self.assertEqual(receipts[0]['returncode'], failed.returncode)
                self.assertEqual(receipts[0]['stdout'], failed.stdout)
                self.assertEqual(receipts[0]['stderr'], failed.stderr)
                self.assertEqual(receipts[0]['argv'][3], 'add-context')
            finally:
                values[9].set()
                values[8].join(timeout=2)

    def test_file_transport_preserves_authored_bytes_and_actual_wrapper_error(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)/'repo'; (root/'plan').mkdir(parents=True)
            facts=root/planning_authoring.FACTS; facts.parent.mkdir(parents=True)
            facts.write_text(json.dumps({'writable_paths':['plan/design.md']}))
            envelope={'public_input':{'profile':'delivery_solution_planning'},'owner_result':{'sentinel':'AI fields'},
                'file_updates':{'plan/design.md':'AI-authored complete text\n'}}
            def run(argv, **kwargs):
                self.assertEqual(json.loads(Path(argv[argv.index('--owner-result')+1]).read_text()), envelope['owner_result'])
                return subprocess.CompletedProcess(argv, 2, '', 'current original diagnostic')
            with patch.object(planning_authoring.subprocess,'run',side_effect=run):
                result=planning_authoring.execute(root,root,envelope,os.environ.copy())
            self.assertEqual((root/'plan/design.md').read_text(),'AI-authored complete text\n')
            self.assertEqual(result.returncode,2)
            self.assertEqual(result.stderr,'current original diagnostic')
            with self.assertRaisesRegex(ValueError,'selected Delivery'):
                planning_authoring.execute(root,root,{**envelope,'file_updates':{'product.py':'unexpected'}}, {})

if __name__=='__main__':
    unittest.main()
