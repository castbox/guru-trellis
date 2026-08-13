from __future__ import annotations
import json, os, subprocess, sys, unittest
from pathlib import Path
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

PACKAGE=Path(__file__).resolve().parents[1]; SKILLS=PACKAGE.parents[1]
if str(SKILLS) not in sys.path: sys.path.insert(0,str(SKILLS))
from runtime.command import main

def validate(path: Path, instance: object):
    schema=json.loads(path.read_text()); schema['$id']=path.as_uri()
    def retrieve(uri: str):
        target=Path(uri.removeprefix('file://')).resolve()
        return Resource.from_contents(json.loads(target.read_text()))
    registry=Registry(retrieve=retrieve).with_resource(path.as_uri(),Resource.from_contents(schema))
    return list(Draft202012Validator(schema,registry=registry).iter_errors(instance))

class ContractTest(unittest.TestCase):
    def test_interface_commands_errors_and_examples_close(self):
        interface=json.loads((PACKAGE/'interface.json').read_text()); commands=json.loads((PACKAGE/'commands.json').read_text()); catalog=json.loads((PACKAGE/'errors/catalog.json').read_text())
        self.assertEqual([],validate(SKILLS/'schemas/skill-interface-1.4.schema.json',interface)); self.assertEqual([],validate(SKILLS/'schemas/skill-commands.schema.json',commands)); self.assertEqual([],validate(SKILLS/'schemas/skill-error-catalog.schema.json',catalog))
        self.assertEqual([],validate(SKILLS/'schemas/skill-evals.schema.json',json.loads((PACKAGE/'evals/evals.json').read_text())))
        self.assertEqual(6,len(interface['external_exits'])); self.assertEqual(5,len(commands['commands']))
        for profile in interface['public_contracts']['input']['profiles']:
            self.assertEqual([],validate(PACKAGE/profile['schema']['path'],json.loads((PACKAGE/profile['example']['path']).read_text())))
        for output in interface['public_contracts']['outputs']:
            self.assertEqual([],validate(PACKAGE/output['schema']['path'],json.loads((PACKAGE/output['example']['path']).read_text())))
    def test_profiles_are_closed_and_not_interchangeable(self):
        post=json.loads((PACKAGE/'examples/public-post-plan-input.json').read_text())
        self.assertTrue(validate(PACKAGE/'schemas/public-post-check-input.schema.json',post))
        post['caller_continuity']={}
        self.assertTrue(validate(PACKAGE/'schemas/public-post-plan-input.schema.json',post))
        post_commit=json.loads((PACKAGE/'examples/public-post-commit-input.json').read_text())
        self.assertNotIn('branch_review_commit',post_commit)
        self.assertEqual([],validate(PACKAGE/'schemas/public-post-commit-input.schema.json',post_commit))
        post_commit['branch_review_commit']=post_commit['task_head']
        self.assertTrue(validate(PACKAGE/'schemas/public-post-commit-input.schema.json',post_commit))
    def test_launchers_and_runtime_are_package_local(self):
        interface=json.loads((PACKAGE/'interface.json').read_text())
        for validator in interface['validators']:
            path=PACKAGE/validator['command']; self.assertTrue(os.access(path,os.X_OK),path); self.assertIn('source "$LAUNCHER" '+validator['runtime_command'],path.read_text())
        for path in list((PACKAGE/'runtime').glob('*.py'))+list((PACKAGE/'scripts').glob('*')):
            self.assertNotIn('guru_team_trellis.py',path.read_text())
    def test_help_is_side_effect_free(self):
        for command in json.loads((PACKAGE/'commands.json').read_text())['commands']:
            with self.subTest(command=command['id']): self.assertEqual(0,main(PACKAGE,[command['id'],'--help']))

if __name__=='__main__': unittest.main()
