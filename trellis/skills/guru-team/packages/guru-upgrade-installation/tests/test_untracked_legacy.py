"""Original Upgrade preview + actual installed Plan2 on old untracked records.

The existing fixture stubs its preset boundary. This proves public per-record
defer/no-write disposition, not old Guru adoption or complete migration.
"""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import test_delivery_upgrade as fixtures


class UntrackedLegacyTests(unittest.TestCase):
    def test_old_official_untracked_nonterminal_task_has_supported_defer_preview(self):
        environment = {k: v for k, v in os.environ.items()
                       if not k.startswith(('TRELLIS_', 'CODEX_', 'CLAUDE_', 'CURSOR_', 'GIT_'))}
        environment['TRELLIS_CONTEXT_ID'] = 'guru548-old-task'
        with patch.dict(os.environ, environment, clear=True):
            fixture = fixtures.DeliveryUpgradeTests('test_prospective_preview_is_zero_write_and_preserves_old_active_root')
            # Official legacy Task writers did not create Guru's current C4
            # binding. Do not add that unrelated fixture projection here.
            fixture.bind_task = lambda *args: None
            fixture.setUp()
            self.addCleanup(fixture.doCleanups)
            version = (fixture.root / '.trellis/.version').read_text().strip()
            self.assertTrue(version.startswith('0.6.'), version)
            fixture.execute([sys.executable, '.trellis/scripts/task.py', 'create', 'Old untracked original Task',
                '--description', 'Original nonterminal planning', '--slug', 'untracked-original', '--no-start'])
            task = next((fixture.root / '.trellis/tasks').glob('*untracked-original'))
            ref = task.relative_to(fixture.root).as_posix()
            for name in ('prd.md', 'design.md', 'implement.md'):
                (task / name).write_text('Original untracked planning: ' + name + '\n')
            for kind in ('implement', 'check'):
                fixture.execute([sys.executable, '.trellis/scripts/task.py', 'add-context', ref, kind,
                                 '.trellis/workflow.md', 'Original legacy workflow'])
            (fixture.root / 'app.txt').write_text('Retained ordinary dirty business content\n')
            (fixture.root / 'user-note.txt').write_text('Retained ordinary untracked content\n')
            self.assertEqual(json.loads((task / 'task.json').read_text())['status'], 'planning')
            committed = subprocess.run(['git', 'cat-file', '-e', 'HEAD:' + ref + '/task.json'], cwd=fixture.root, capture_output=True)
            self.assertNotEqual(committed.returncode, 0)
            self.assertIn('?? ' + ref + '/', fixture.git('status', '--short', '--', ref))

            plan = fixture.plan(deferred_workspaces=('primary',))
            core = plan['core_plan']
            core['source'].update(version=version, task_schema='legacy')
            # The owner explicitly preserves every retired predecessor receipt
            # asset; the 0.6 CLI has platform entries absent from Task1 fixtures.
            owned = {row['target'].get('path') for row in core['files'] if row['target'].get('workspace') == 'primary'}
            receipt = json.loads((fixture.root / '.trellis/.template-hashes.json').read_text())
            for name in receipt['hashes']:
                if name not in owned:
                    core['files'].append({'target': {'kind': 'project', 'workspace': 'primary', 'path': name},
                                          'owner': 'preserve', 'action': 'preserve', 'source': fixture.raw(fixture.root, name)})
            row = next(row for row in core['tasks'] if row['task_ref'] == ref)
            self.assertEqual(row['disposition'], 'defer')
            self.assertNotIn('record', row)
            before = fixture.tree()
            head, refs, worktrees = fixture.git('rev-parse', 'HEAD'), fixture.git('show-ref'), fixture.git('worktree', 'list', '--porcelain')
            inventory = fixtures.upgrade.prepare_inventory(fixture.root, fixture.fork)
            selected = next(row for row in inventory['workspaces'][0]['tasks'] if row['task_ref'] == ref)
            self.assertEqual(selected['source'], fixture.raw(fixture.root, ref + '/task.json'))
            preview = fixtures.upgrade.preview(fixtures.PACKAGE, fixture.root, fixture.public, plan, fixture.fork)
            self.assertEqual(preview['core']['status'], 'preview')
            action = next(a for a in preview['core']['actions'] if Path(a['path']).resolve() == (task / 'task.json').resolve())
            self.assertEqual(action['action'], 'preserve')
            self.assertEqual(action['before_sha256'], action['after_sha256'])
            self.assertEqual(action['before_mode'], action['after_mode'])
            self.assertEqual(fixture.tree(), before)
            self.assertEqual((fixture.git('rev-parse', 'HEAD'), fixture.git('show-ref'), fixture.git('worktree', 'list', '--porcelain')),
                             (head, refs, worktrees))
            self.assertNotIn('schema_version', json.loads((task / 'task.json').read_text()))
            # Preview contains no conversion/Delivery/planning authority for
            # this missing-HEAD original. It has not restored execution.
            self.assertNotIn('deliveries', json.loads((task / 'task.json').read_text()))


if __name__ == '__main__':
    unittest.main()
