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

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import task_free_authoring, native_adapter
from adapters.eval.eval_support import qualification_trace_helper_source, stage_public_projection
from adapters.eval.fixture_io import run_git, stage_clean_installed_owner_repo

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
PACKAGE = SKILLS / 'packages/guru-execute-task-free-change'


def stage(root: Path, case_id: str):
    case = next(row for row in json.loads((PACKAGE / 'evals/evals.json').read_text())['evals'] if row['id'] == case_id)
    workdir = root / 'execution/workdir'
    workdir.mkdir(parents=True)
    for relative in case['files']:
        target = workdir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(PACKAGE / relative, target)
    request = {'skill_id': PACKAGE.name, 'case_id': case_id,
               'package_root': str(PACKAGE), 'workdir': str(workdir), 'files': case['files']}
    fixture, source = stage_clean_installed_owner_repo(
        workdir.parent, REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
    package = fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name
    task_free_authoring.stage(request, fixture, package, source)
    return fixture, package


class TaskFreeAuthoringTests(unittest.TestCase):
    def test_qualifier_helper_forwards_original_envelopes_to_actual_wrappers(self):
        # Deterministic transport input only; no native semantic verdict is
        # supplied to an evaluated Agent or inferred from wrapper acceptance.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            repo, package = stage(root, 'native-owner-qualification-pair')
            facts = json.loads((repo / task_free_authoring.FACTS).read_text())
            for name in ('normal-scenario', 'solution-mechanism', 'root-cause'):
                path = f'.trellis/guru-team/skills/consumers/workflow/production/{name}-qualification-invocation.schema.json'
                self.assertIn(path, facts['required_reads'])
                self.assertTrue((repo / path).is_file())
            import threading
            stop = threading.Event()
            request_fifo, response_fifo = root / 'request', root / 'response'
            observations=task_free_authoring.ObservationCommands(repo,root/'observation-receipts.json')
            thread = native_adapter.start_qualification_runtime_boundary(
                request_fifo, response_fifo, stop, repo, package, {}, {}, observation_commands=observations)
            helper = root / 'helper.py'
            helper.write_text(qualification_trace_helper_source(allow_commands=True))
            trace = root / 'trace.json'
            interface=json.loads((PACKAGE/'interface.json').read_text())
            request={'skill_id':PACKAGE.name,'case_id':'native-owner-qualification-pair',
                'package_root':str(PACKAGE),'native_execution_mode':'semantic_authoring',
                'workdir':str(root/'work'),'files':[],
                'interface':{'public_invocation':interface['public_contracts']['invocation']}}
            projected,skill_path,wrapper_path,skill_hash,wrapper_hash=stage_public_projection(request,root)
            (root/'evidence/case').mkdir(parents=True)
            argv = [sys.executable, '-B', str(helper), '--trace', str(trace),
                '--request-sha256', '1' * 64, '--projection-root', str(projected),
                '--repository-root', str(repo), '--sandbox-root', str(root),
                '--request-fifo', str(request_fifo), '--response-fifo', str(response_fifo),
                '--skill-sha256', skill_hash, '--wrapper-sha256', wrapper_hash]
            public = {'profile':'task_free_pre_write','mode':'workflow','caller':task_free_authoring.SKILL,
                'target_locator':task_free_authoring.PUBLIC_INPUT, 'target':facts['qualification_target'],
                'candidate_refs':['transport-fixture'],
                'candidate_locators':[{'candidate_ref':'transport-fixture','locators':['catalog.py']}]}
            try:
                for relative in task_free_authoring.PUBLIC_READS:
                    read=subprocess.run([*argv,'read','--kind','skill_contract','--path',str(projected/relative)],
                        capture_output=True,text=True,check=False)
                    self.assertEqual(read.returncode,0,read.stderr)
                for relative in [task_free_authoring.FACTS,*facts['required_reads'],task_free_authoring.PUBLIC_INPUT]:
                    read=subprocess.run([*argv,'read','--kind','owner_file','--path',str(repo/relative)],
                        capture_output=True,text=True,check=False)
                    self.assertEqual(read.returncode,0,read.stderr)
                unsupported=subprocess.run([*argv,'command','--skill-id','task-free-authoring','--command','status'],
                    input='',cwd=repo,capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(unsupported.returncode,2)
                self.assertTrue(thread.is_alive())
                help_result=subprocess.run([*argv,'command','--skill-id','task-free-authoring','--command','help'],
                    input='',cwd=repo,capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(help_result.returncode,0,help_result.stderr)
                self.assertIn('--command inspect',help_result.stdout)
                inspected=subprocess.run([*argv,'command','--skill-id','task-free-authoring','--command','inspect'],
                    input='',cwd=repo,capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(inspected.returncode,0,inspected.stderr)
                position=json.loads(inspected.stdout)
                self.assertEqual(position['cwd'],str(repo.resolve()))
                self.assertEqual(position['git_observations']['head']['stdout'].strip(),run_git(repo,'rev-parse','HEAD'))
                self.assertEqual(position['task_record_locators'],[])
                source = (repo / 'docs/display-help.md').read_text()
                changed = source + '\nTransport write observation.\n'
                written = subprocess.run([*argv,'command','--skill-id','task-free-authoring','--command','write','--stdin'],
                    input=json.dumps({'file_updates':{'docs/display-help.md':changed}}),cwd=repo,
                    capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(written.returncode,0,written.stderr)
                self.assertEqual((repo/'docs/display-help.md').read_text(),changed)
                check_code = 'from pathlib import Path; import sys; assert Path("docs/display-help.md").read_text() == sys.argv[1]'
                checked = subprocess.run([*argv,'command','--skill-id','task-free-authoring','--command','run','--stdin'],
                    input=json.dumps({'argv':[sys.executable,'-B','-c',check_code,source]}),
                    cwd=repo,capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(checked.returncode,0,checked.stderr)
                actual = json.loads(checked.stdout)
                self.assertEqual(actual['returncode'],1)
                self.assertIn('AssertionError',actual['stderr'])
                rechecked = subprocess.run([*argv,'command','--skill-id','task-free-authoring','--command','run','--stdin'],
                    input=json.dumps({'argv':[sys.executable,'-B','-c',check_code,changed]}),
                    cwd=repo,capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(rechecked.returncode,0,rechecked.stderr)
                self.assertEqual(json.loads(rechecked.stdout)['returncode'],0)
                restored = subprocess.run([*argv,'command','--skill-id','task-free-authoring','--command','write','--stdin'],
                    input=json.dumps({'file_updates':{'docs/display-help.md':source}}),cwd=repo,
                    capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(restored.returncode,0,restored.stderr)
                for name in ('normal-scenario', 'solution-mechanism', 'root-cause'):
                    semantic = {'schema_version':'1.0','skill_id':'guru-qualify-' + name,
                        'public_input':public, 'candidate_results':[{'candidate_ref':'transport-fixture',
                            'decision':'rejected_not_reproduced','reason':'Objective wrapper transport fixture.',
                            'witness':{'requirement_refs':['docs/catalog-contract.md'],
                                'supported_entry_refs':['catalog.py'], 'existing_caller_refs':['test_catalog.py'],
                                'honest_action_sequence':['Run the supplied operation fixture.'],
                                'defect_observation':'No semantic defect is asserted by this transport test.',
                                'excluded_assumptions':[]}}],
                        'ai_review_gate':{'status':'passed','reviewed_candidate_refs':['transport-fixture'],
                            'summary':'Objective transport input; native judgment is separate.'},
                        'typed_exit':'classified','consumer':{'kind':'workflow','id':'guru-' + name + '-classified-router'}}
                    if name=='root-cause':
                        semantic['candidate_results']=[{'candidate_ref':'transport-fixture','goal':'ordinary_feature',
                            'classification':'not_incident_applicable','reason':'Objective original wrapper transport only.',
                            'evidence':{'applicability_basis':'This unit input tests transport; native judgment is separate.'}}]
                    envelope = {'schema_version':'1.0','semantic_result':semantic}
                    result = subprocess.run([*argv,'invoke','--stdin','--qualifier',name],
                        input=json.dumps(envelope),cwd=repo,capture_output=True,text=True,check=False,timeout=20)
                    self.assertEqual(result.returncode,0,result.stderr or result.stdout)
                    self.assertEqual(json.loads(result.stdout)['exit_id'],'classified')
                invocation=json.loads((repo/task_free_authoring.PUBLIC_INPUT).read_text())
                owner={key:invocation[key] for key in ('mode','continuation_id','selection_origin','request_summary','target_paths')}
                owner.update(schema_version='1.0',typed_exit='blocked',
                    pre_write_review={'status':'blocked','summary':'Objective transport fixture; native semantics are separate.'},
                    ai_review_gate={'status':'blocked','summary':'No semantic adequacy is claimed by this transport test.'})
                final=subprocess.run([*argv,'invoke','--stdin'],input=json.dumps({'public_input':invocation,'owner_result':owner}),
                    cwd=repo,capture_output=True,text=True,check=False,timeout=20)
                self.assertEqual(final.returncode,0,final.stderr or final.stdout)
                events=json.loads(trace.read_text())['events']
                invokes=[event for event in events if event['kind']=='invoke']
                self.assertEqual(len(invokes),4)
                self.assertEqual([Path(event['wrapper_path']).parents[1].name for event in invokes[:-1]],
                    ['guru-qualify-normal-scenario','guru-qualify-solution-mechanism','guru-qualify-root-cause'])
                self.assertTrue(all(event['returncode']==0 for event in invokes))
                task_free_authoring.validate_observations([event for event in events if event['kind']=='command'],
                    {'task_free_observation_receipts_path':str(root/'observation-receipts.json')},'1'*64)
                protocol={'projection_root':str(projected),'skill_path':str(skill_path),
                    'skill_sha256':skill_hash,'wrapper_sha256':wrapper_hash,
                    'owner_repository':str(repo),'repository_projection_root':str(repo),'model_root':str(root),
                    'semantic_authoring':True,'task_free_observation_receipts_path':str(root/'observation-receipts.json')}
                protocol_path=root/'protocol.json';protocol_path.write_text(json.dumps(protocol))
                native_adapter.validate_native_trace(trace,'1'*64,request,wrapper_path,final.stdout.strip(),protocol_path)
            finally:
                stop.set()
                thread.join(timeout=2)

    def test_actual_operations_and_unqualified_target_state(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, package = stage(Path(temp), 'native-owner-qualification-pair')
            facts = json.loads((repo / task_free_authoring.FACTS).read_text())
            rows = json.loads((repo / '.trellis/task-free-eval/operations.json').read_text())
            self.assertEqual([row['returncode'] for row in rows], [0, 1])
            self.assertEqual(rows[0]['after']['display_title'], 'Readable title')
            self.assertEqual(rows[0]['before']['active_target'], rows[0]['after']['active_target'])
            self.assertEqual(rows[1]['before'], rows[1]['after'])
            self.assertTrue((repo / '.git').is_file())
            self.assertEqual(run_git(repo, 'branch', '--show-current'), 'task-free-candidate')
            self.assertFalse((repo / '.trellis/tasks').exists())
            self.assertNotIn('typed_exit', json.dumps(facts))
            self.assertNotIn('expected_exit', json.dumps(facts))
            self.assertFalse((repo / '.trellis/.runtime/guru-team/evals/owner-result.json').exists())
            self.assertTrue(all((repo / path).is_file() for path in facts['required_reads']))
            self.assertEqual(json.loads((repo / '.trellis/task-free-eval/validation.json').read_text())['returncode'], 0)
            public = json.loads((repo / task_free_authoring.PUBLIC_INPUT).read_text())
            owner = {key: public[key] for key in ('mode', 'continuation_id', 'selection_origin', 'request_summary', 'target_paths')}
            owner.update(schema_version='1.0', typed_exit='completed',
                pre_write_review={'status': 'suitable', 'summary': 'Test transport input for actual linked position.'},
                ai_review_gate={'status': 'passed', 'summary': 'Test transport only; native owner judgment is separate.'},
                completion_evidence={'edited_paths': ['docs/display-help.md'],
                    'targeted_checks': [{'command': 'python -B -m unittest -v test_catalog', 'status': 'passed', 'summary': 'Three actual catalog tests passed.'}],
                    'post_write_review': {'status': 'passed', 'summary': 'Test transport is bounded to one guide.'},
                    'unverified_boundaries': ['Native semantic evaluation is separate.']})
            result = task_free_authoring.execute(package, repo, {'public_input': public, 'owner_result': owner,
                'file_updates': {'docs/display-help.md': '# Catalog display\n\nUpdated guide.\n'}}, dict(os.environ))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['exit_id'], 'completed')
            receipts = json.loads((repo.parent / 'task-free-command-receipts.json').read_text())
            self.assertEqual(len(receipts), 3)
            self.assertEqual((repo / 'docs/display-help.md').read_text(), '# Catalog display\n\nUpdated guide.\n')
            self.assertFalse((repo / '.trellis/.runtime/guru-team/evals/task-free-authoring.json').exists())

    def test_shared_candidate_green_tests_and_partial_start(self):
        with tempfile.TemporaryDirectory() as temp:
            repo, _ = stage(Path(temp), 'native-owner-shared-restriction')
            rows = json.loads((repo / '.trellis/task-free-eval/operations.json').read_text())
            self.assertEqual([row['returncode'] for row in rows], [0, 1, 1, 1])
            self.assertEqual(rows[2]['before'], rows[2]['after'])
            self.assertEqual(rows[3]['before'], rows[3]['after'])
            validation = json.loads((repo / '.trellis/task-free-eval/candidate-validation.json').read_text())
            self.assertEqual(validation['returncode'], 0, validation['stderr'])
            self.assertEqual(run_git(repo, 'diff', '--name-only'), 'docs/display-help.md')
            self.assertEqual(run_git(repo, 'diff', '--', 'catalog.py'), '')
            facts = json.loads((repo / task_free_authoring.FACTS).read_text())
            self.assertEqual(facts['prior_edited_paths'], ['docs/display-help.md'])
            self.assertNotIn('owner_result', json.dumps(facts))


if __name__ == '__main__':
    unittest.main()
