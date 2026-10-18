"""Author validation uses installed public identity; writing remains AI-owned."""
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE.parent / 'guru-create-delivery/tests'))
from support import installed_fixture, owner_module
from runtime.io import CommandError


class RuntimeTest(unittest.TestCase):
    def setUp(self):
        self.fixture = installed_fixture(self)
        self.module = owner_module(PACKAGE)
        self.key = self.fixture.create()
        self.directory = self.fixture.projection.planning_directory(self.key)

    def public(self, profile):
        value = json.loads((PACKAGE / 'examples' / ('public-' + profile.replace('_', '-') + '-input.json')).read_text())
        value['task_ref'] = self.fixture.task_ref
        if profile.startswith('delivery_'):
            value['delivery_key'] = self.key
        return value

    def invoke(self, public, output):
        owner = {'public_input': public, 'output': output,
                 'ai_review_gate': {'status': 'passed', 'summary': 'Local transport fixture, semantic review is separate.'}}
        with patch.object(self.module, '_task', return_value=self.fixture.task):
            return self.module.execute(PACKAGE, self.fixture.root, public, owner)

    def test_scope_only_has_no_delivery_or_future_design_precondition(self):
        self.fixture.stop(self.key)
        public = self.public('task_scope_requirements')
        output = {'exit_id': 'scope_requirements_ready', 'task_ref': self.fixture.task_ref,
                  'requirements_locator': self.fixture.task_ref + '/prd.md'}
        before = {p.name: p.read_bytes() for p in self.fixture.task.iterdir() if p.is_file()}
        self.assertEqual(output, self.invoke(public, output))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.fixture.task.iterdir() if p.is_file()})
        with self.assertRaises(CommandError):
            self.invoke(public, {'exit_id': 'plan_ready', 'task_ref': self.fixture.task_ref, 'delivery_key': self.key})

    def test_first_delivery_requirements_need_no_future_design(self):
        public = self.public('delivery_initial_review')
        before = (self.directory / 'design.md').read_bytes()
        (self.directory / 'prd.md').write_text('Current independent slice requirements')
        output = {'exit_id': 'requirements_ready', 'task_ref': self.fixture.task_ref, 'delivery_key': self.key,
                  'candidate': {'design_facts': ['One existing owner.'], 'constraint_refs': ['docs/source.md#Design']}}
        self.assertEqual(output, self.invoke(public, output))
        self.assertEqual((self.directory / 'design.md').read_bytes(), before)

    def test_plan_handoff_reads_only_selected_delivery_and_official_context(self):
        public = self.public('delivery_solution_planning')
        output = {'exit_id': 'plan_ready', 'task_ref': self.fixture.task_ref, 'delivery_key': self.key}
        for name in ('prd.md', 'design.md', 'implement.md'):
            (self.directory / name).write_text('Current Delivery planning')
        for name in ('implement.jsonl', 'check.jsonl'):
            (self.directory / name).write_text(json.dumps({'file': '.trellis/spec/workflow/index.md', 'reason': 'Current contract'})+'\n')
        before = {p.name: p.read_bytes() for p in self.directory.iterdir() if p.is_file()}
        self.assertEqual(output, self.invoke(public, output))
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.directory.iterdir() if p.is_file()})
        (self.directory / 'check.jsonl').write_text('{}\n')
        with self.assertRaises(CommandError):
            self.invoke(public, output)

    def test_requirements_locator_cannot_use_task_root_as_delivery_plan(self):
        public = self.public('delivery_initial_review')
        (self.directory / 'prd.md').write_text('Slice requirements')
        (self.fixture.task / 'design.md').write_text('Old Task-root design')
        with self.assertRaises(CommandError) as caught:
            self.invoke(public, {'exit_id': 'requirements_ready', 'task_ref': self.fixture.task_ref, 'delivery_key': self.key,
                                 'candidate': {'design_locator': self.fixture.task_ref + '/design.md'}})
        self.assertEqual(caught.exception.code, 'stale_identity')

    def test_migrated_empty_official_context_is_preserved_but_missing_context_blocks(self):
        public = self.public('delivery_solution_planning')
        output = {'exit_id': 'plan_ready', 'task_ref': self.fixture.task_ref, 'delivery_key': self.key}
        for name in ('prd.md', 'design.md', 'implement.md'):
            (self.directory / name).write_text('Current Delivery planning')
        for name in ('implement.jsonl', 'check.jsonl'):
            (self.directory / name).write_bytes(b'')
        self.assertEqual(output, self.invoke(public, output))
        self.assertEqual(b'', (self.directory / 'implement.jsonl').read_bytes())
        (self.directory / 'check.jsonl').unlink()
        with self.assertRaises(CommandError):
            self.invoke(public, output)

    def test_original_requirements_profiles_still_require_candidate_assessment(self):
        for profile in ('delivery_initial_review', 'delivery_active_task_scope_change', 'delivery_requirements_revision', 'delivery_architecture_conflict_resolution'):
            with self.subTest(profile=profile), self.assertRaises(CommandError):
                self.invoke(self.public(profile), {'exit_id': 'plan_ready', 'task_ref': self.fixture.task_ref, 'delivery_key': self.key})

    def test_other_delivery_and_legacy_profiles_do_not_replace_current_identity(self):
        public = self.public('delivery_initial_review')
        self.fixture.stop(self.key)
        other = self.fixture.create()
        (self.directory / 'prd.md').write_text('D1 retained requirements')
        with self.assertRaises(CommandError) as caught:
            self.invoke(public, {'exit_id': 'requirements_ready', 'task_ref': self.fixture.task_ref, 'delivery_key': self.key,
                                 'candidate': {'design_facts': ['Existing owner.'], 'constraint_refs': ['docs/source.md']}})
        self.assertEqual(caught.exception.code, 'stale_identity')
        self.assertEqual(self.fixture.projection.current()['key'], other)
        public['profile'] = 'initial_review'
        with self.assertRaises(CommandError):
            self.invoke(public, {'exit_id': 'blocked', 'task_ref': self.fixture.task_ref, 'missing_refs': ['legacy profile']})
