"""Native context/trace projection integration for the original eval transports."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from adapters.eval import native_adapter
from adapters.eval.eval_support import qualification_trace_helper_source
SKILLS=Path(__file__).resolve().parents[2]
REPO=SKILLS.parents[2]


def request(root, skill, case_id):
    package=SKILLS/'packages'/skill
    case=next(c for c in json.loads((package/'evals/evals.json').read_text())['evals'] if c['id']==case_id)
    work=root/'execution/workdir';work.mkdir(parents=True)
    for relative in case['files']:
        target=work/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(package/relative,target)
    interface=json.loads((package/'interface.json').read_text())
    return {**{k:case[k] for k in ('prompt','files','model_id','native_execution_mode','native_execution_adapter')},
        'schema_version':'1.0','skill_id':skill,'case_id':case_id,'package_root':str(package),
        'workdir':str(work),'runtime_target':str(REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh'),
        'interface':{'public_invocation':interface['public_contracts']['invocation']}}


class NativeConstraintTransportTests(unittest.TestCase):
    def test_task_free_model_projection_has_actual_contracts_and_qualifier_targets(self):
        with tempfile.TemporaryDirectory() as temp:
            req=request(Path(temp),'guru-execute-task-free-change','native-owner-qualification-pair')
            values=native_adapter.build_context(req,'codex')
            try:
                protocol=json.loads(values[4].read_text())
                module=native_adapter.additional_authoring_module(req['skill_id'])
                package=Path(protocol['projection_root'])
                for path in module.PUBLIC_READS:self.assertTrue((package/path).is_file(),path)
                repo=Path(protocol['repository_projection_root'])
                facts=json.loads((repo/module.FACTS).read_text())
                self.assertTrue(all((repo/path).is_file() for path in facts['required_reads']))
                self.assertIsNone(protocol['architecture_context'])
                self.assertIn('--qualifier normal-scenario',values[0])
                self.assertIn('--qualifier root-cause',values[0])
                self.assertIn('intentionally has no .git',values[0])
                self.assertIn('command inspect',values[0])
                self.assertTrue(protocol['task_free_observation_receipts_path'])
                self.assertIn('.trellis/guru-team/skills/consumers/workflow/production/root-cause-qualification-invocation.schema.json',facts['required_reads'])
                self.assertIn(str(repo/module.FACTS),values[0])
                self.assertTrue(protocol['writable_preimages'])
                native=json.loads(values[5].read_text())
                self.assertNotIn('expected_exit',native)
                self.assertNotIn('assertions',native)
            finally:values[9].set();values[8].join(timeout=2)

    def test_implementation_private_commands_do_not_add_a_public_flow(self):
        for skill,case in [('guru-author-task-plan','native-implementation-plan-premise'),
                           ('guru-clarify-requirements','native-implementation-authority-conflict'),
                           ('guru-check-task','native-implementation-code-drift')]:
            with self.subTest(case=case),tempfile.TemporaryDirectory() as temp:
                req=request(Path(temp),skill,case)
                values=native_adapter.build_context(req,'codex')
                try:
                    protocol=json.loads(values[4].read_text())
                    self.assertTrue(protocol['implementation_commands'])
                    self.assertIsNone(protocol['architecture_context'])
                    self.assertIsNone(protocol['native_authoring_flow'])
                    self.assertIn('COMMAND_FORWARDING_ALLOWED = True',Path(protocol['helper_path']).read_text())
                    module=native_adapter.additional_authoring_module(skill,case)
                    package=Path(protocol['projection_root'])
                    for path in module.public_reads(package):self.assertTrue((package/path).is_file(),path)
                    facts=json.loads((Path(protocol['repository_projection_root'])/module.FACTS).read_text())
                    self.assertTrue(facts['owner_mutated_paths'])
                    self.assertIn('command --skill-id',values[0])
                finally:values[9].set();values[8].join(timeout=2)
        self.assertIn('COMMAND_FORWARDING_ALLOWED = False',qualification_trace_helper_source())

if __name__=='__main__':unittest.main()
