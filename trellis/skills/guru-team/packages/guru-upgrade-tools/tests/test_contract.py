from __future__ import annotations
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
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
        self.assertEqual([x['id'] for x in interface['public_contracts']['input']['profiles']], ['install', 'resume', 'rollback'])
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
        projected = {m['target']: output[m['source']] for m in row['mappings']}
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
