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

PACKAGE = Path(__file__).resolve().parents[2] / 'packages/guru-maintain-architecture-baseline'


class ArchitectureAuthoringTests(unittest.TestCase):
    def fixture(self, root, case='planning-semantic-authoring', stage='planning'):
        repo = root / 'repository'
        repo.mkdir()
        subprocess.run(['git', 'init', '-q', '-b', 'main', str(repo)], check=True)
        for name, value in (('user.name', 'Eval'), ('user.email', 'eval@example.invalid')):
            subprocess.run(['git', '-C', str(repo), 'config', name, value], check=True)
        work = root / 'work'
        (work / 'evals/files').mkdir(parents=True)
        public = json.loads((PACKAGE / 'evals/files/impact-current-input.json').read_text())
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
            self.assertFalse((repo / '.trellis/.runtime').exists())
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
        for kind in ("sufficient", "insufficient"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                repo = self.fixture(Path(temp), case=f"planning-constraint-{kind}-native")
                facts = json.loads((repo / ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
                leaf = '.trellis/tasks/eval-task/constraints.md'
                self.assertIn(leaf, facts['required_reads'])
                self.assertTrue((repo / leaf).is_file())
                self.assertIn("protocol='wire_v2'", (repo / 'transport.py').read_text())
                self.assertIn("protocol='responses'", (repo / 'query_summary.py').read_text())
                self.assertFalse((repo / '.trellis/tasks/eval-task/prd.md').exists())
                self.assertFalse((repo / '.trellis/tasks/eval-task/implement.md').exists())
                self.assertNotIn('typed_exit', json.dumps(facts))

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
