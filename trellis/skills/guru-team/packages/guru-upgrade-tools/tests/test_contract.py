from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from jsonschema import Draft202012Validator

PACKAGE = Path(__file__).resolve().parents[1]
SKILLS = PACKAGE.parents[1]
sys.path.insert(0, str(SKILLS))
sys.path.insert(0, str(PACKAGE / 'runtime'))
import tools_owner as owner

class ToolsContractTests(unittest.TestCase):
    def test_each_public_profile_and_exit_has_independent_valid_example(self):
        interface = json.loads((PACKAGE / 'interface.json').read_text())
        for contract in interface['public_contracts']['input']['profiles'] + interface['public_contracts']['outputs']:
            schema = json.loads((PACKAGE / contract['schema']['path']).read_text())
            example = json.loads((PACKAGE / contract['example']['path']).read_text())
            Draft202012Validator(schema).validate(example)
        self.assertEqual([x['id'] for x in interface['public_contracts']['input']['profiles']], ['install', 'resume', 'rollback', 'recover_frozen_source'])
        self.assertEqual(interface['judgment_mode'], 'semantic')
        self.assertEqual(interface['modes']['workflow']['routing'], 'not_applicable')
        self.assertEqual(interface['ordered_stages'], ['forward_behavior','ai_review_gate','conditional_human_confirmation','recorder_validator','typed_exit'])
        description = (PACKAGE / 'SKILL.md').read_text().split('description: ', 1)[1].split('\n', 1)[0]
        self.assertEqual(description, interface['description'])

    def test_resume_transports_only_original_owner_reference(self):
        schema = json.loads((PACKAGE / 'schemas/public-resume-input.schema.json').read_text())
        self.assertEqual(set(schema['properties']), {'profile', 'recovery_ref'})
        output = json.loads((PACKAGE / 'examples/public-resume_required-output.json').read_text())
        self.assertEqual(set(output), {'exit_id','profile','recovery_ref'})
        interface = json.loads((PACKAGE / 'interface.json').read_text())
        row = next(x for x in interface['public_contracts']['projections'] if x['exit_id']=='resume_required')
        projected = {m['target']: output[m['source']] for m in row['mappings'] if m['source'] in output}
        Draft202012Validator(schema).validate(projected)

    def fixture(self, base):
        root = base / 'repo'; root.mkdir()
        for args in [('init','-q','-b','main'), ('config','user.email','fixture@example.invalid'), ('config','user.name','Fixture')]:
            subprocess.run(['git',*args], cwd=root, check=True, capture_output=True)
        (root/'app').write_text('business')
        subprocess.run(['git','add','.'],cwd=root,check=True,capture_output=True)
        subprocess.run(['git','commit','-qm','fixture'],cwd=root,check=True,capture_output=True)
        return root.resolve()

    def test_explicit_checkout_does_not_depend_on_current_branch_or_task(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.fixture(Path(d))
            (root/'app').write_text('legitimate dirty business')
            self.assertEqual(owner.selected_target(root, {'checkout':str(root)}), root)
            self.assertFalse((root/'.trellis').exists())

    def test_ordered_branch_is_chosen_before_checkout_availability(self):
        with tempfile.TemporaryDirectory() as d:
            root=self.fixture(Path(d))
            subprocess.run(['git','branch','dev'],cwd=root,check=True,capture_output=True)
            # dev exists but has no checkout: main must not silently win.
            with self.assertRaises(Exception): owner.selected_target(root, {})
            self.assertEqual(subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip(),'main')

    def test_whole_tool_store_alias_is_rejected_before_write(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);root=self.fixture(base)
            shared=base/'store';shared.mkdir();(root/'.trellis').symlink_to(shared,target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'Whole-.trellis'):
                owner.isolated_layout(root,owner.legacy_owner(PACKAGE))
            self.assertEqual(list(shared.iterdir()),[])

    def test_prunable_missing_git_peer_is_skipped_without_touching_residue(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            root = self.fixture(base)
            root_tools = root / '.trellis'
            root_tools.mkdir()
            stale = base / 'stale'
            stale.mkdir()
            marker = stale / 'residue'
            marker.write_bytes(b'preserve')
            (stale / '.trellis').symlink_to(root_tools, target_is_directory=True)
            stale_without_colon = base / 'stale-without-colon'
            stale_without_colon.mkdir()
            marker_without_colon = stale_without_colon / 'residue'
            marker_without_colon.write_bytes(b'preserve too')
            (stale_without_colon / '.trellis').symlink_to(root_tools, target_is_directory=True)
            normal = base / 'normal'
            normal.mkdir()
            (normal / '.git').mkdir()
            prunable_valid = base / 'prunable-valid'
            prunable_valid.mkdir()
            (prunable_valid / '.git').mkdir()
            prunable_link = base / 'prunable-link'
            prunable_link.mkdir()
            (prunable_link / '.git').symlink_to(base / 'missing-git-target')
            records = [
                f'worktree {root}',
                f'worktree {stale}\nprunable: gitdir file points to non-existent location',
                f'worktree {stale_without_colon}\nprunable gitdir file points to non-existent location',
                f'worktree {normal}',
                f'worktree {prunable_valid}\nprunable',
                f'worktree {prunable_link}\nprunable',
            ]
            porcelain = '\n\n'.join(records) + '\n'
            rev_parse_paths = []

            def git(cwd, *args):
                if args == ('worktree', 'list', '--porcelain'):
                    return porcelain
                if args == ('rev-parse', '--git-common-dir'):
                    return str(root / '.git')
                if args == ('rev-parse', '--absolute-git-dir'):
                    path = Path(cwd).resolve()
                    rev_parse_paths.append(path)
                    return str(path / '.git')
                raise AssertionError(args)

            old = SimpleNamespace(git=git, state=lambda path: None)
            pointers = owner.peer_pointers(root, old)
            owner.isolated_layout(root, old)

            self.assertNotIn(stale.resolve(), rev_parse_paths)
            self.assertNotIn(stale_without_colon.resolve(), rev_parse_paths)
            self.assertIn(normal.resolve(), rev_parse_paths)
            self.assertIn(prunable_valid.resolve(), rev_parse_paths)
            self.assertIn(prunable_link.resolve(), rev_parse_paths)
            self.assertFalse(any(str(stale) in pointer for pointer in pointers))
            self.assertFalse(any(str(stale_without_colon) in pointer for pointer in pointers))
            self.assertTrue(stale.is_dir())
            self.assertEqual(marker.read_bytes(), b'preserve')
            self.assertTrue(stale_without_colon.is_dir())
            self.assertEqual(marker_without_colon.read_bytes(), b'preserve too')

    def test_missing_git_without_prunable_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            root = self.fixture(base)
            damaged = base / 'damaged'
            damaged.mkdir()
            porcelain = f'worktree {root}\n\nworktree {damaged}\n'
            rev_parse_paths = []

            def git(cwd, *args):
                if args == ('worktree', 'list', '--porcelain'):
                    return porcelain
                if args == ('rev-parse', '--git-common-dir'):
                    return str(root / '.git')
                if args == ('rev-parse', '--absolute-git-dir'):
                    path = Path(cwd).resolve()
                    rev_parse_paths.append(path)
                    if path == damaged.resolve():
                        raise subprocess.CalledProcessError(128, ['git', 'rev-parse', '--absolute-git-dir'])
                    return str(path / '.git')
                raise AssertionError(args)

            old = SimpleNamespace(git=git, state=lambda path: None)
            with self.assertRaises(subprocess.CalledProcessError):
                owner.peer_pointers(root, old)
            self.assertIn(damaged.resolve(), rev_parse_paths)

    def test_frozen_retry_projection_preserves_the_original_action_and_reference(self):
        interface = json.loads((PACKAGE / 'interface.json').read_text())
        row = next(x for x in interface['public_contracts']['projections']
                   if x['exit_id'] == 'frozen_recovery_required')
        profile = next(x for x in interface['public_contracts']['input']['profiles']
                       if x['id'] == 'recover_frozen_source')
        schema = json.loads((PACKAGE / profile['schema']['path']).read_text())
        for action in ('resume', 'rollback'):
            output = json.loads((PACKAGE / 'examples/public-frozen_recovery_required-output.json').read_text())
            output['action'] = action
            projected = {m['target']: output[m['source']] for m in row['mappings'] if m['source'] in output}
            Draft202012Validator(schema).validate(projected)
            self.assertEqual(projected, {'profile': 'recover_frozen_source', 'action': action,
                                         'recovery_ref': output['recovery_ref']})

    def test_retired_locations_are_not_an_input_to_same_source_recovery(self):
        public = {'profile': 'resume', 'recovery_ref': '11111111-1111-4111-8111-111111111111',
                  'retired_peer_roots': []}
        with self.assertRaises(owner.CommandError) as error:
            owner.run(PACKAGE, {'runtime_role': 'invoke'}, ['--root', '.', '--input', json.dumps(public)])
        self.assertEqual(error.exception.code, 'schema_mismatch')
