"""Objective fresh-worker, candidate and transport regressions; no pass simulation."""
from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import architecture_authoring as authoring
from adapters.eval.eval_constants import ARCHITECTURE_PUBLIC_AUTHORING_FACTS
from adapters.eval.fixture_io import run_git, stage_clean_installed_owner_repo

PACKAGE = Path(__file__).resolve().parents[2] / 'packages/guru-maintain-architecture-baseline'


class ArchitectureAuthoringTests(unittest.TestCase):
    def test_followup_evidence_arrives_only_after_actual_first_invocation(self):
        for kind in ('refresh', 'unchanged'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                repo = self.fixture(root, case=f'planning-constraint-{kind}-native')
                model = root / 'projection'
                shutil.copytree(repo, model, ignore=shutil.ignore_patterns('.git'))
                later = 'docs/architecture-eval/provider-followup.md'
                self.assertFalse((repo / later).exists())
                before = (repo / 'transport.py').read_bytes()
                reveal = authoring.stage_followup({'case_id': f'planning-constraint-{kind}-native'}, repo, model, root / 'private')
                reveal(subprocess.CompletedProcess([], 0, '{"exit_id":"baseline_current"}', ''))
                self.assertEqual((repo / later).read_bytes(), (model / later).read_bytes())
                self.assertEqual((repo / 'transport.py').read_bytes(), before)
                self.assertIn('asynchronous' if kind == 'refresh' else 'No provider lifecycle', (repo / later).read_text())
                events = [{'kind':'invoke'}, {'kind':'read','path':str(model / later)}, {'kind':'invoke'}]
                authoring.validate_followup_reads(events, model)
                with self.assertRaisesRegex(ValueError, 'between'):
                    authoring.validate_followup_reads([events[1], events[0], events[2]], model)

    def fixture(self, root, case='planning-semantic-authoring', stage='planning'):
        source = PACKAGE.parents[4]
        repo, _ = stage_clean_installed_owner_repo(root,
            source / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
        repo = repo.resolve()
        run_git(repo, 'add', '.')
        run_git(repo, 'commit', '-qm', 'stage installed Architecture fixture tools')
        work = root / 'work'
        (work / 'evals/files').mkdir(parents=True)
        input_file = ('impact-current-input.json' if stage == 'planning' else
            'branch-review-independent-native-input.json' if stage == 'branch_review' else
            'implementation-discovery-independent-native-input.json')
        public = json.loads((PACKAGE / 'evals/files' / input_file).read_text())
        public['stage'] = stage
        (work / 'evals/files/input.json').write_text(json.dumps(public))
        authoring.stage_architecture_facts({'workdir': str(work), 'files': ['evals/files/input.json'], 'case_id': case}, repo)
        return repo

    def test_real_candidate_and_unchanged_consumers_have_no_task_narratives_or_prefilled_result(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = self.fixture(Path(temp))
            facts = json.loads((repo / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
            self.assertEqual(facts['required_reads'][:3], [
                'docs/architecture/00-foundation/design-constitution.md',
                'docs/architecture/README.md', 'docs/architecture/06-governance/change-contract.md',
            ])
            for relative in facts['required_reads']:
                self.assertTrue((repo / relative).is_file(), relative)
                self.assertNotIn(Path(relative).name, {'prd.md', 'implement.md', 'task.json'})
            self.assertFalse((repo / '.trellis/.runtime/guru-team/evals/owner-result.json').exists())
            self.assertIn('query_summary.py', facts['required_reads'])
            self.assertIn('import_pipeline.py', facts['required_reads'])
            diff = (repo / 'docs/architecture-eval/candidate.patch').read_text()
            self.assertIn('dict(payload=payload', diff)
            self.assertNotIn('query_summary.py', diff)
            self.assertNotIn('typed_exit', json.dumps(facts))
            self.assertNotIn('expected_exit', json.dumps(facts))

    def test_committed_range_is_actual_git_candidate_not_phase2_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = self.fixture(Path(temp), stage='branch_review')
            inventory = json.loads((repo / 'docs/architecture-eval/candidate-inventory.json').read_text())
            self.assertNotEqual(inventory['base_head'], inventory['review_head'])
            self.assertIn('transport.py', (repo / inventory['tracked_diff']).read_text())
            actual = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
            self.assertEqual(inventory['review_head'], actual)

    def test_nonplanning_candidate_binding_remains_current_after_fact_staging(self):
        from runtime.reviewed_content import reviewed_content_identity
        from runtime.schema import validate_json
        with tempfile.TemporaryDirectory() as temp:
            repo = self.fixture(Path(temp), stage='implementation_discovery')
            facts = json.loads((repo / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
            public = json.loads((repo / facts['public_input_locator']).read_text())
            validate_json(public, PACKAGE / 'schemas/public-input-delivery-task-impact-sync-4.0.schema.json', 'input')
            self.assertEqual('guru-maintain-architecture-baseline:6.0', public['project_contract']['guru_contract_identity'])
            self.assertIn('schemas/semantic-result-delivery-4.0.schema.json', authoring.contract_paths(public))
            self.assertEqual(public['candidate']['content_identity'], 'sha256:' + reviewed_content_identity(repo)['sha256'])
            self.assertEqual(public['before_authority']['git_revision'], public['candidate']['head'])
            (repo / 'query_summary.py').write_text('A changed unchanged-consumer dependency\n')
            self.assertNotEqual(public['candidate']['content_identity'], 'sha256:' + reviewed_content_identity(repo)['sha256'])

    def test_current_closeout_and_planning_keep_their_exact_contract_versions(self):
        from runtime.schema import validate_json
        with tempfile.TemporaryDirectory() as temp:
            repo = self.fixture(Path(temp), stage='planning')
            facts = json.loads((repo / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
            planning = json.loads((repo / facts['public_input_locator']).read_text())
            validate_json(planning, PACKAGE / 'schemas/public-input-delivery-task-impact-sync-1.0.schema.json', 'planning')
            self.assertEqual('delivery-1.0', planning['schema_version'])
            self.assertIn('schemas/semantic-result-delivery-1.0.schema.json', authoring.contract_paths(planning))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / 'repository'
            repo.mkdir()
            run_git(repo, 'init', '-q', '-b', 'main')
            run_git(repo, 'config', 'user.name', 'Eval')
            run_git(repo, 'config', 'user.email', 'eval@example.invalid')
            work = root / 'work'; work.mkdir()
            current = json.loads((PACKAGE / 'evals/files/branch-review-independent-native-input.json').read_text())
            current.update(schema_version='6.0', profile='task_impact_sync', stage='acceptance_finish')
            for field in ('delivery_key', 'planning_root', 'committed_range'):
                current.pop(field, None)
            input_path = work / 'input.json'; input_path.write_text(json.dumps(current))
            request = {'workdir':str(work), 'files':['input.json'], 'case_id':'current-closeout-transport'}
            authoring.stage_architecture_facts(request, repo)
            facts = json.loads((repo / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
            staged = json.loads((repo / facts['public_input_locator']).read_text())
            validate_json(staged, PACKAGE / 'schemas/public-input-impact-nonplanning-6.0.schema.json', 'closeout')
            self.assertEqual('6.0', staged['schema_version'])
            self.assertEqual('guru-maintain-architecture-baseline:6.0', staged['project_contract']['guru_contract_identity'])
            self.assertIn('schemas/semantic-result-6.0.schema.json', authoring.contract_paths(staged))
            # A historical input is not reinterpreted as the current operation.
            current['schema_version'] = '5.0'
            input_path.write_text(json.dumps(current))
            head = run_git(repo, 'rev-parse', 'HEAD')
            with self.assertRaisesRegex(ValueError, 'historical inputs are not upgraded'):
                authoring.stage_architecture_facts(request, repo)
            self.assertEqual(head, run_git(repo, 'rev-parse', 'HEAD'))

    def test_business_candidate_source_tests_and_proposed_contribution_are_consistent(self):
        for case in ('planning-business-default-native', 'planning-inherited-business-default-native'):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp:
                repo = self.fixture(Path(temp), case=case)
                facts = json.loads((repo / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
                validation = json.loads((repo / 'docs/architecture-eval/candidate-test-result.json').read_text())
                self.assertEqual(validation['returncode'], 0, validation['stderr'])
                self.assertIn('Ran 3 tests', validation['stderr'])
                self.assertIn("metric_stage='import_stage2'", (repo / 'import_pipeline.py').read_text())
                diff = (repo / 'docs/architecture-eval/candidate.patch').read_text()
                self.assertIn('import_pipeline.py', diff)
                self.assertNotIn('query_summary.py', diff)
                contribution = facts['candidate_contribution_locator']
                self.assertNotIn(contribution, facts['required_reads'])
                self.assertIn('Import callers supply a stage', (repo / contribution).read_text())
                self.assertNotIn('review', (repo / contribution).read_text())
                self.assertIn('test_transport_candidate.py', facts['required_reads'])

    def test_no_candidate_has_no_design_or_diff_and_does_not_stage_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = self.fixture(Path(temp), case='planning-missing-candidate-native')
            inventory = json.loads((repo / 'docs/architecture-eval/candidate-inventory.json').read_text())
            self.assertIsNone(inventory['design_locator'])
            self.assertEqual((repo / inventory['tracked_diff']).read_text().strip(), '')

    def test_minimal_task_constraints_are_real_candidate_facts_without_narrative(self):
        for kind in ("sufficient", "insufficient", "refuted"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                repo = self.fixture(Path(temp), case=f"planning-constraint-{kind}-native")
                facts = json.loads((repo / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
                inventory = json.loads((repo / 'docs/architecture-eval/candidate-inventory.json').read_text())
                leaf = str(Path(inventory['design_locator']).parent / 'constraints.md')
                self.assertIn(leaf, facts['required_reads'])
                self.assertTrue((repo / leaf).is_file())
                self.assertIn("protocol='wire_v2'", (repo / 'transport.py').read_text())
                self.assertIn("protocol='responses'", (repo / 'query_summary.py').read_text())
                self.assertFalse((repo / '.trellis/tasks/eval-task/prd.md').exists())
                self.assertFalse((repo / '.trellis/tasks/eval-task/implement.md').exists())
                self.assertNotIn('typed_exit', json.dumps(facts))
                if kind == 'refuted':
                    self.assertIn('asynchronous job identifier', (repo / leaf).read_text())
                    self.assertIn('assumes wire_v2 returns the completed response', (repo / inventory['design_locator']).read_text())

    def test_reviewer_launch_is_separate_ephemeral_process_with_actual_error_preserved(self):
        original = ['codex', 'exec', '--ephemeral', '--output-last-message', '/overall.txt', 'overall owner task narrative']
        error = subprocess.CompletedProcess([], 2, '', 'provider unavailable')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            visible_context = root / 'native-context.txt'
            visible_context.write_text(original[-1])

            def execute(command, **kwargs):
                self.assertEqual(visible_context.read_text(), command[-1])
                self.assertNotIn('overall owner task narrative', visible_context.read_text())
                self.assertEqual(kwargs['input'], '')
                return error

            with patch.object(authoring.subprocess, 'run', side_effect=execute) as run:
                result = authoring.execute_reviewer(original, Path('/reviewer.txt'), 'authority/candidate locators', cwd=root, environment={})
        self.assertIs(result, error)
        self.assertEqual(original[-1], 'overall owner task narrative')
        self.assertEqual(run.call_args.args[0][-1], 'authority/candidate locators')
        self.assertIn('/reviewer.txt', run.call_args.args[0])
        with self.assertRaisesRegex(ValueError, 'fresh ephemeral'):
            authoring.execute_reviewer(['codex', 'exec', 'resume'], Path('/unused'), '', cwd=Path('/fixture'), environment={})

    def test_supported_worker_read_sequence_detects_missing_consumer_and_early_narrative(self):
        repo = Path('/repository')
        reads = ['constitution.md', 'baseline.md', 'change-contract.md', 'candidate.patch', 'unchanged_caller.py']
        events = [{'kind': 'read', 'path': str(repo / path)} for path in reads]
        events.append({'kind': 'invoke'})
        authoring.validate_reviewer_reads(events, repo, reads, phase2=True)
        with self.assertRaisesRegex(ValueError, 'candidate or consumer'):
            authoring.validate_reviewer_reads(events[:-2] + events[-1:], repo, reads, phase2=True)
        with self.assertRaisesRegex(ValueError, 'task narrative'):
            authoring.validate_reviewer_reads([{'kind': 'read', 'path': '/repository/task/prd.md'}, *events], repo, reads, phase2=True)
        with self.assertRaisesRegex(ValueError, 'authority before'):
            authoring.validate_reviewer_reads([events[3], *events[:3], *events[4:]], repo, reads, phase2=True)
        with self.assertRaisesRegex(ValueError, 'authority before'):
            authoring.validate_reviewer_reads([*events[:2], events[3], events[2], *events[4:]], repo, reads, phase2=True)

    def test_persistent_reviewer_is_a_new_exec_with_empty_stdin_and_original_failure(self):
        command = ['codex', 'exec', '--output-last-message', '/overall.txt', 'overall narrative']
        error = subprocess.CompletedProcess(command, 9, 'partial output', 'original failure')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            public_input = root / 'public-input.json'
            public_input.write_text('{}')
            with patch.object(authoring, 'public_contract_reads', return_value=[]):
                original_context = authoring.reviewer_context(root, root, 'original helper', [],
                    public_input, upstream=False)
                persistent_context = authoring.reviewer_context(root, root, 'original helper', [],
                    public_input, upstream=False, persisted_observation=True)
            self.assertEqual(persistent_context,
                original_context.replace('fresh ephemeral', 'fresh independent'))
            with self.assertRaisesRegex(ValueError, 'fresh ephemeral'):
                authoring.execute_reviewer(command, root / 'result', 'independent context',
                    cwd=root, environment={})
            with patch.object(authoring.subprocess, 'run', return_value=error) as run:
                actual = authoring.execute_reviewer(command, root / 'result', 'independent context',
                    cwd=root, environment={}, allow_persisted=True)
                self.assertIs(actual, error)
                self.assertEqual(run.call_args.args[0], [*command[:-3], '--output-last-message',
                    str(root / 'result'), 'independent context'])
                self.assertEqual(run.call_args.kwargs['input'], '')
                self.assertEqual((root / 'native-context.txt').read_text(), 'independent context')
                for history in ('resume', 'fork'):
                    with self.subTest(history=history), self.assertRaisesRegex(ValueError, 'fresh ephemeral'):
                        authoring.execute_reviewer(['codex', 'exec', history, '--output-last-message',
                            '/unused', ''], root / 'result', '', cwd=root, environment={}, allow_persisted=True)
                self.assertEqual(run.call_count, 1)

    def test_exact_method_contracts_can_overlap_without_hiding_candidate_evidence(self):
        repo = Path('/repository')
        public = json.loads((PACKAGE / 'evals/files/branch-review-independent-native-input.json').read_text())
        package = repo / '.trellis/guru-team/skills/packages' / PACKAGE.name
        contracts = [package / path.relative_to(PACKAGE)
            for path in authoring.public_contract_reads(PACKAGE, public)]
        overlaps = [package / path for path in ('SKILL.md', 'interface.json',
            'references/contract.md', 'schemas/public-input-delivery-task-impact-sync-4.0.schema.json')]
        self.assertTrue(set(overlaps).issubset(contracts))
        authorities = ['constitution.md', 'baseline.md', 'change-contract.md']
        # The changed object may itself be a method contract. Its full diff
        # and actual consumer still supply separate evidence after authority.
        evidence = ['changed-contract.patch', 'unchanged_caller.py']
        reads = [*authorities, *(p.relative_to(repo).as_posix() for p in overlaps), *evidence]
        paths = [*contracts, *(repo / p for p in authorities), *(repo / p for p in evidence)]
        events = [{'kind': 'read', 'path': str(path)} for path in paths] + [{'kind': 'invoke'}]
        validate = lambda rows: authoring.validate_reviewer_reads(rows, repo, reads,
            phase2=True, contract_reads=contracts)
        validate(events)
        with self.assertRaisesRegex(ValueError, 'required contract'):
            validate([e for e in events if e.get('path') != str(contracts[-1])])
        with self.assertRaisesRegex(ValueError, 'candidate or consumer'):
            validate([e for e in events if e.get('path') != str(repo / evidence[0])])
        with self.assertRaisesRegex(ValueError, 'one exact Skill'):
            validate([events[1], events[0], *events[2:]])
        with self.assertRaisesRegex(ValueError, 'one exact Skill'):
            validate([events[0], *events])
        for relative in evidence:
            with self.subTest(early=relative), self.assertRaisesRegex(ValueError, 'authority before'):
                early = {'kind': 'read', 'path': str(repo / relative)}
                validate([events[0], early, *events[1:]])
        start = len(contracts)
        with self.assertRaisesRegex(ValueError, 'authority order'):
            validate([*events[:start], events[start + 1], events[start], *events[start + 2:]])

    def test_phase2_continues_only_from_actual_current_upstream_result(self):
        process = subprocess.CompletedProcess([], 0, '', '')
        for exit_id in ('baseline_current', 'blocked', 'architecture_conflict', 'baseline_incomplete'):
            output = json.dumps({'exit_id': exit_id})
            events = [{'kind': 'invoke', 'returncode': 0,
                       'stdout_sha256': hashlib.sha256(output.encode()).hexdigest()}]
            with self.subTest(exit=exit_id):
                if exit_id == 'baseline_current':
                    authoring.validate_phase2_predecessor(process, output, events)
                else:
                    with self.assertRaisesRegex(ValueError, 'requires actual upstream Architecture baseline_current'):
                        authoring.validate_phase2_predecessor(process, output, events)
                with self.assertRaisesRegex(ValueError, 'actual wrapper output'):
                    authoring.validate_phase2_predecessor(subprocess.CompletedProcess([], 2, '', 'error'), output, events)


if __name__ == '__main__':
    unittest.main()
