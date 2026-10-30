"""Verify fact staging, unchanged consumers and answer isolation through real adapters."""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import architecture_authoring, native_adapter, stage_result_authoring
from runtime.delivery_projection.adapter import DeliveryProjection

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]


def case_request(root, skill, case):
    package = SKILLS / 'packages' / skill
    row = next(row for row in json.loads((package / 'evals/evals.json').read_text())['evals']
               if row['id'] == case)
    work = root / 'execution/workdir'
    work.mkdir(parents=True)
    for relative in row['files']:
        destination = work / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(package / relative, destination)
    interface = json.loads((package / 'interface.json').read_text())
    return {'schema_version':'1.0', 'skill_id':skill, 'case_id':case,
        'package_root':str(package), 'prompt':row['prompt'], 'files':row['files'],
        'workdir':str(work), 'interface':{'public_invocation':interface['public_contracts']['invocation']},
        'runtime_target':str(REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh'),
        'native_execution_mode':'semantic_authoring', 'native_execution_adapter':'codex',
        'model_id':row['model_id']}


class MechanismTransportTests(unittest.TestCase):
    def test_architecture_projection_carries_declared_consumer_schemas_and_refs(self):
        from adapters.eval.eval_support import stage_public_projection, schema_projection_closure
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = case_request(root, 'guru-maintain-architecture-baseline', 'native-mechanism-coordination')
            package = Path(request['package_root'])
            interface = json.loads((package / 'interface.json').read_text())
            contracts = interface['public_contracts']
            declared = {Path(row['schema']['path']) for row in contracts['outputs']}
            declared.update(Path(row['contract']['path']) for row in contracts['consumer_inputs'])
            required_before = architecture_authoring.public_contract_reads(package)
            projection, *_ = stage_public_projection(request, root / 'projection-test')
            for relative in schema_projection_closure(package, declared):
                self.assertEqual((projection / relative).read_bytes(), (package / relative).read_bytes(), relative)
            self.assertFalse(any(path.relative_to(package).parts[0] == 'consumers' for path in required_before))
            self.assertFalse((projection / 'evals').exists())
            self.assertFalse((projection / 'runtime').exists())

    def test_three_architecture_candidates_preserve_before_after_and_no_host_answer(self):
        for name in ('cursor', 'coordination', 'reuse'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                request = case_request(root, 'guru-maintain-architecture-baseline', 'native-mechanism-' + name)
                repo = root / 'repository'
                repo.mkdir()
                subprocess.run(['git','init','-q','-b','main',str(repo)],check=True)
                for key,value in (('user.name','Eval'),('user.email','eval@example.invalid')):
                    subprocess.run(['git','-C',str(repo),'config',key,value],check=True)
                (repo / '.trellis').mkdir()
                shutil.copy2(REPO / '.trellis/workflow.md', repo / '.trellis/workflow.md')
                architecture_authoring.stage_architecture_facts(request, repo)
                facts=json.loads((repo / architecture_authoring.ARCHITECTURE_PUBLIC_AUTHORING_FACTS).read_text())
                bundle=json.loads((Path(request['workdir']) / request['files'][1]).read_text())
                for relative in facts['required_reads']:
                    self.assertTrue((repo / relative).is_file(),relative)
                for relative,body in bundle['baseline_files'].items():
                    before=subprocess.check_output(['git','show','HEAD:'+relative],cwd=repo,text=True)
                    self.assertEqual(before,body)
                for relative,body in bundle['candidate_files'].items():
                    self.assertEqual((repo / relative).read_text(),body)
                self.assertNotIn('expected_exit',json.dumps(bundle))
                self.assertFalse((repo / '.trellis/.runtime/guru-team/evals/owner-result.json').exists())
                public=json.loads((repo / facts['public_input_locator']).read_text())
                design=repo / public['candidate']['design_locator']
                self.assertEqual(public['freshness_identity'],'sha256:'+hashlib.sha256(design.read_bytes()).hexdigest())
                if name=='reuse':
                    diff=(repo / 'docs/architecture-eval/candidate.patch').read_text()
                    self.assertNotIn('diff --git a/transport.py',diff)
                    self.assertIn('search_entry.py',facts['required_reads'])

    def test_completion_uses_actual_delivered_slice_and_keeps_whole_scope_pending(self):
        with tempfile.TemporaryDirectory() as temporary:
            request=case_request(Path(temporary),'guru-review-task-completion','native-stage-mechanism-stock')
            values=native_adapter.build_context(request,'codex')
            try:
                protocol=json.loads(values[4].read_text())
                owner=Path(protocol['owner_repository'])
                facts=json.loads((owner / stage_result_authoring.FACTS).read_text())
                projection=DeliveryProjection(owner,facts['task_ref'])
                record=projection.read_record()
                self.assertEqual(record['completion_results'],[])
                self.assertEqual(projection.resolve(facts['delivery_key'])['phase'],'delivered')
                scope_body = (owner / facts['task_ref'] / 'prd.md').read_text()
                bundle = json.loads((Path(request['workdir']) / request['files'][1]).read_text())
                self.assertIn(bundle['whole_task_scope'], scope_body)
                self.assertEqual(record['accepted_scope']['revision'],
                                 'sha256:' + hashlib.sha256(scope_body.encode()).hexdigest())
                for relative in ('legacy_writer.py','new_writer.py','writer_observation.json','docs/migration-facts.md'):
                    self.assertIn(relative,facts['required_reads'])
                    self.assertTrue((owner / relative).is_file())
                observed=json.loads((owner / 'writer_observation.json').read_text())
                self.assertIsNone(observed['later_delivery']['delivery_result'])
                self.assertNotIn('expected_exit',(owner / stage_result_authoring.FACTS).read_text())
            finally:
                values[9].set()
                values[8].join(timeout=2)


if __name__=='__main__':
    unittest.main()
