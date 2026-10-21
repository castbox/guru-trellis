from __future__ import annotations

import json
import hashlib
import ast
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import architecture_authoring, delivery_production, implementation_authoring, native_adapter
from adapters.eval.eval_support import qualification_trace_helper_source, stage_repository_projection, repository_file_inventory
from adapters.eval.fixture_io import stage_clean_installed_owner_repo, run_git
from runtime.delivery_projection.adapter import DeliveryProjection
from adapters.eval.owner_runtime import load_package_runtime_module

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
PACKAGE = SKILLS / 'packages/guru-author-task-plan'


class ImplementationAuthoringTests(unittest.TestCase):
    def assert_rdt_command_reaches_original_wrapper(self, fixture, facts):
        # A complete public request reaches the original owner's structural
        # validation. No native semantic result or no-change answer is supplied.
        source_bytes = (fixture / 'docs/range.md').read_bytes()
        public = {'schema_version':'2.0','profile':'task_impact_sync',
            'source_exit':'implementation_complete','mode':'workflow','continuation_id':'rdt-transport-only',
            'stage':'phase2','task_locator':facts['task_ref'],'authority_locator':'docs/range.md',
            'authority_version':'range-rdt-v1','authority_freshness':hashlib.sha256(source_bytes).hexdigest(),
            'task_delta_locator':'docs/phase2-evidence/diff.patch','applicability_scope':'R1 range predicate/filter',
            'architecture_baseline':{'locator':'docs/architecture/README.md','version':'range-v1','status':'active'}}
        before = repository_file_inventory(fixture)
        relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ),
            fixture.parent / 'rdt-transport-receipts.json')
        result = relay.forward({'skill_id':implementation_authoring.RDT,'command':'invoke',
            'arguments':['--invocation',json.dumps({'public_input':public,'owner_result':{}})],'stdin':''})
        self.assertNotEqual(result['returncode'],0)
        error = json.loads(result['stdout'])
        self.assertEqual(error['code'],'schema_mismatch')
        self.assertTrue(error['field_path'].startswith('owner_result'),error)
        self.assertEqual(repository_file_inventory(fixture),before)
        self.assertTrue(relay.terminal)
        required = facts['required_reads']
        prefix = '.trellis/guru-team/skills/packages/' + implementation_authoring.RDT + '/'
        for relative in ('SKILL.md','interface.json','commands.json','references/contract.md',
                'references/current-knowledge.md','schemas/public-input-impact-2.0.schema.json',
                'schemas/semantic-result.schema.json'):
            self.assertIn(prefix + relative, required)
            self.assertTrue((fixture / (prefix + relative)).is_file())

    def test_plan_and_authority_sources_exist_before_original_acceptance(self):
        for case_id, test_names in (
                ('native-implementation-plan-premise',{'test_lower_and_interior','test_upper_and_singleton','test_outside'}),
                ('native-implementation-authority-conflict',{'test_endpoints_and_interior','test_outside','test_singleton','test_negative'})):
            with self.subTest(case_id=case_id), tempfile.TemporaryDirectory() as temporary:
                fixture, source = stage_clean_installed_owner_repo(Path(temporary) / 'execution',
                    REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
                fixture = fixture.resolve()
                seed = {}
                original_identity = architecture_authoring.stage_delivery_identity
                original_activate = delivery_production.activate
                def capture_identity(repository, public, **options):
                    seed['before_scope'] = (repository / 'docs/range.md').read_bytes()
                    return original_identity(repository, public, **options)
                def capture_activation(runtime, repository, task, key, **options):
                    seed['before_planning'] = (repository / 'docs/range.md').read_bytes()
                    seed['tests'] = (repository / 'test_interval.py').read_bytes()
                    seed['architecture'] = {relative:(repository / relative).read_bytes() for relative in (
                        'docs/architecture/README.md','docs/architecture/00-foundation/design-constitution.md')}
                    result = original_activate(runtime, repository, task, key, **options)
                    seed['after_acceptance'] = (repository / 'docs/range.md').read_bytes()
                    return result
                with patch.object(architecture_authoring,'stage_delivery_identity',side_effect=capture_identity), \
                        patch.object(delivery_production,'activate',side_effect=capture_activation):
                    implementation_authoring.stage({'case_id':case_id},fixture,
                        fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name,source)
                authority = (fixture / 'docs/range.md').read_bytes()
                self.assertEqual(authority,seed['before_scope'])
                self.assertEqual(authority,seed['before_planning'])
                self.assertEqual(authority,seed['after_acceptance'])
                self.assertIn(b'Identity: range-rdt-v1',authority)
                for relative, content in seed['architecture'].items():
                    self.assertEqual((fixture / relative).read_bytes(),content)
                self.assertIn(b'interval.py owns a pure predicate',seed['architecture']['docs/architecture/README.md'])
                self.assertIn(b'mathematical interval evaluation',
                    seed['architecture']['docs/architecture/00-foundation/design-constitution.md'])
                tree = ast.parse(seed['tests'])
                actual_tests = {node.name for node in ast.walk(tree)
                    if isinstance(node,ast.FunctionDef) and node.name.startswith('test_')}
                self.assertEqual(actual_tests,test_names)
                facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
                design = (fixture / facts['planning_root'] / 'design.md').read_text()
                validation = json.loads((fixture / 'docs/phase2-evidence/validation.json').read_text())
                if case_id == 'native-implementation-plan-premise':
                    self.assertIn('lower <= value < upper',design)
                    self.assertIn(b'self.assertFalse(contains(4, 2, 4))',seed['tests'])
                    self.assertIn(b'self.assertFalse(contains(2, 2, 2))',seed['tests'])
                    self.assertEqual(validation['returncode'],0,validation['stderr'])
                else:
                    self.assertIn('integer comparisons',design)
                    self.assertNotEqual(validation['returncode'],0)
                self.assert_rdt_command_reaches_original_wrapper(fixture,facts)

    def test_original_approval_commands_change_only_current_delivery_checkpoint(self):
        # This executes deterministic owner transport, not native inference.
        with tempfile.TemporaryDirectory() as temporary:
            fixture, source = stage_clean_installed_owner_repo(Path(temporary) / 'execution',
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            fixture = fixture.resolve()
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'}, fixture,
                fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name, source)
            self.assertIn('mathematical interval evaluation',
                (fixture / 'docs/architecture/00-foundation/design-constitution.md').read_text())
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            projection = DeliveryProjection(fixture, facts['task_ref'])
            key = facts['delivery_key']
            from runtime.delivery_projection.gates import rework
            rework(projection, key, 'implementation', 'planning',
                projection.resolve(key)['scope_ref']['authority'],
                ['planning','check','full_review','readiness'])
            task = fixture / facts['task_ref']
            public = {'profile':'delivery_initial_review','mode':'workflow',
                'task_ref':facts['task_ref'],'delivery_key':key,'source_exit':'baseline_current',
                'architecture_assessment':delivery_production.final_architecture(
                    fixture, task, key, preserve_existing_constitution=True)}
            example = json.loads((SKILLS / 'packages/guru-approve-task-plan/examples/planning-approval-delivery.json').read_text())
            authored = {name:example[name] for name in ('mode','authority_refs','delivery_policy',
                'docs_ssot_plan','semantic_review','typed_exit','consumer','reason')}
            authored['authority_refs'] = ['docs/range.md']
            authored['delivery_policy'].update(task_scope=['R1'],delivery_slice=['R1'],remaining_work=[],
                remaining_work_owner='No deferred scope in this deterministic transport fixture.')
            authored['docs_ssot_plan'].update(durable_paths=['docs/range.md'],
                summary='Original recorder transport fixture; no native Docs judgment is asserted.')
            authored['semantic_review']['summary'] = 'Original owner transport only; no native approval is asserted.'
            authored['reason'] = 'Deterministic inventory regression for the original Approval commands.'
            input_path = Path(temporary) / 'approval-input.json'
            input_path.write_text(json.dumps(authored))
            before = repository_file_inventory(fixture)
            relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ),
                fixture.parent / 'approval-receipts.json')
            recorded = relay.forward({'skill_id':'guru-approve-task-plan','command':'record-planning-approval',
                'arguments':['--task',facts['task_ref'],'--delivery-key',json.dumps(key),
                    '--input',str(input_path)],'stdin':''})
            self.assertEqual(recorded['returncode'],0,recorded['stderr'] or recorded['stdout'])
            receipt = json.loads(recorded['stdout'])['result']
            checkpoint = Path(receipt['artifact_path'])
            relative = checkpoint.relative_to(fixture).as_posix()
            self.assertEqual(relative,
                f".trellis/.runtime/guru-team/owner-checkpoints/{task.name}/{key['delivery_id']}/planning-approval.json")
            self.assertIn(relative, facts['owner_mutated_paths'])
            checked = relay.forward({'skill_id':'guru-approve-task-plan','command':'check-planning-approval',
                'arguments':['--task',facts['task_ref'],'--delivery-key',json.dumps(key),'--require-exit','approved'],
                'stdin':''})
            self.assertEqual(checked['returncode'],0,checked['stderr'] or checked['stdout'])
            owner = json.loads(checkpoint.read_text())
            invoked = relay.forward({'skill_id':'guru-approve-task-plan','command':'invoke',
                'arguments':['--invocation','-'],
                'stdin':json.dumps({'public_input':public,'owner_result':owner})})
            self.assertEqual(invoked['returncode'],0,invoked['stderr'] or invoked['stdout'])
            self.assertEqual(json.loads(invoked['stdout'])['exit_id'],'approved')
            # The declared inline invocation currently leaves the recorder's
            # exact checkpoint; path-based invocation consumes it below.
            self.assertTrue(checkpoint.is_file())
            after = repository_file_inventory(fixture)
            changed = {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}
            self.assertEqual(changed, {relative})
            for path in facts['owner_mutated_paths']:
                before.pop(path,None);after.pop(path,None)
            self.assertEqual(before,after)
            consumed = relay.forward({'skill_id':'guru-approve-task-plan','command':'invoke',
                'arguments':['--input','-','--owner-result',relative],'stdin':json.dumps(public)})
            self.assertEqual(consumed['returncode'],0,consumed['stderr'] or consumed['stdout'])
            self.assertEqual(json.loads(consumed['stdout']),json.loads(invoked['stdout']))
            self.assertFalse(checkpoint.exists())
            self.assertFalse(relay.terminal)

    def test_code_drift_original_activation_binds_complete_unmodified_seed(self):
        # Observe the real original seed/Planning/Approval/Activation sequence.
        # Its acceptance is a fixture precondition, not a native semantic result.
        with tempfile.TemporaryDirectory() as temporary:
            fixture, source = stage_clean_installed_owner_repo(Path(temporary) / 'execution',
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            seed = {}
            business_paths = ('interval.py','range_filter.py','test_interval.py','docs/range.md',
                'docs/architecture/README.md','docs/architecture/00-foundation/design-constitution.md',
                'docs/architecture/06-governance/change-contract.md')
            original_activate = delivery_production.activate
            original_identity = architecture_authoring.stage_delivery_identity
            def capture_identity(repository, public, **options):
                seed['before_scope'] = (repository / 'docs/range.md').read_bytes()
                return original_identity(repository, public, **options)
            def capture_activation(runtime, repository, task, key, **options):
                projection = DeliveryProjection(repository, task.relative_to(repository).as_posix())
                planning = projection.planning_directory(key)
                paths = [task / 'prd.md', *[planning / name for name in ('prd.md','design.md','implement.md')]]
                seed['bytes'] = {path.relative_to(repository).as_posix():path.read_bytes() for path in paths}
                seed['implementation'] = (repository / 'interval.py').read_bytes()
                seed['business'] = {relative:(repository / relative).read_bytes() for relative in business_paths}
                seed['activation_head'] = run_git(repository, 'rev-parse', 'HEAD')
                result = original_activate(runtime, repository, task, key, **options)
                seed['delivery'] = projection.resolve(key)
                seed['task'] = json.loads((task / 'task.json').read_text())
                seed['result_id'] = result
                return result
            with patch.object(architecture_authoring,'stage_delivery_identity',side_effect=capture_identity), \
                    patch.object(delivery_production, 'activate', side_effect=capture_activation) as activated:
                implementation_authoring.stage({'case_id':'native-implementation-code-drift'}, fixture,
                    fixture / '.trellis/guru-team/skills/packages/guru-check-task', source)
            activated.assert_called_once()
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            projection = DeliveryProjection(fixture, facts['task_ref'])
            delivery = projection.resolve(facts['delivery_key'])
            self.assertEqual(seed['delivery']['phase'], 'implementing')
            self.assertEqual(delivery['results']['planning'], seed['delivery']['results']['planning'])
            planning_result = delivery['results']['planning']
            self.assertEqual(planning_result['result_id'], seed['result_id'])
            self.assertEqual(planning_result['outcome'], 'accepted')
            for locator, content in seed['bytes'].items():
                self.assertEqual((fixture / locator).read_bytes(), content)
            def ref(locator):
                return {'locator':locator, 'revision':'sha256:' + hashlib.sha256(seed['bytes'][locator]).hexdigest()}
            root_prd = facts['task_ref'] + '/prd.md'
            planning = facts['planning_root']
            self.assertEqual(seed['task']['accepted_scope'], ref(root_prd))
            self.assertEqual(delivery['scope_ref']['authority'], ref(root_prd))
            self.assertEqual(planning_result['plan_ref'], ref(planning + '/design.md'))
            self.assertEqual(planning_result['evidence'], [ref(planning + '/' + name)
                for name in ('prd.md','design.md','implement.md')])
            self.assertEqual(seed['implementation'], b'def contains(value, lower, upper):\n    raise NotImplementedError\n')
            self.assertEqual((fixture / 'interval.py').read_text(),
                'def contains(value, lower, upper):\n    return lower <= value < upper\n')
            base = delivery['candidate']['base_ref']
            self.assertIn(base, (fixture / planning / 'design.md').read_text())
            self.assertEqual(base, run_git(fixture, 'rev-parse', base))
            self.assertNotEqual(base, run_git(fixture, 'rev-parse', 'origin/main'))
            self.assertEqual(base, seed['activation_head'])
            before_bytes = {}
            for relative in business_paths:
                before = subprocess.run(['git','show',f'{base}:{relative}'],cwd=fixture,
                    capture_output=True,check=False)
                self.assertEqual(before.returncode,0,before.stderr.decode())
                before_bytes[relative] = before.stdout
                self.assertEqual(before.stdout,seed['business'][relative])
            self.assertEqual(before_bytes['interval.py'],
                b'def contains(value, lower, upper):\n    raise NotImplementedError\n')
            self.assertIn('includes both endpoints, including singleton ranges',
                before_bytes['docs/range.md'].decode())
            self.assertNotIn(facts['task_ref'] + '/task.json',
                run_git(fixture,'ls-tree','-r','--name-only',base).splitlines())
            self.assertEqual(run_git(fixture,'diff','--name-only',base,'--',*business_paths).splitlines(),
                ['interval.py'])
            self.assertEqual((fixture / planning / 'implement.jsonl').read_bytes(), b'')
            self.assertEqual((fixture / planning / 'check.jsonl').read_bytes(), b'')
            design = (fixture / planning / 'design.md').read_text()
            implementation = (fixture / planning / 'implement.md').read_text()
            self.assertNotIn('## Docs SSOT Plan', design)
            self.assertEqual(implementation.count('## 5. Delivery Policy'), 1)
            self.assertEqual(implementation.count('## 6. Docs SSOT Plan'), 1)
            validation = subprocess.run([sys.executable,'-B','-m','unittest','-v','test_interval'],
                cwd=fixture, capture_output=True, text=True, check=False)
            self.assertNotEqual(validation.returncode, 0)
            self.assertIn('Ran 4 tests', validation.stderr)
            self.assertIn('test_singleton', validation.stderr)
            probe = subprocess.run([sys.executable,'-B','-c',
                'import json; from range_filter import select; print(json.dumps(['
                'select([1,2,3,4,5],2,4),select([1,2,3],2,2),select([4,2,4,1,3],2,4)]))'],
                cwd=fixture, capture_output=True, text=True, check=False)
            self.assertEqual(probe.returncode, 0, probe.stderr)
            self.assertEqual(json.loads(probe.stdout), [[2,3],[],[2,3]])
            self.assertEqual((fixture / 'docs/range.md').read_bytes(),seed['before_scope'])
            self.assert_rdt_command_reaches_original_wrapper(fixture.resolve(),facts)

    def test_original_check_recorder_changes_only_its_declared_checkpoint(self):
        # Recorder input is a deterministic transport fixture, never a native
        # semantic result or evidence supplied to the evaluated Agent.
        with tempfile.TemporaryDirectory() as temporary:
            execution = Path(temporary) / 'execution'
            fixture, source = stage_clean_installed_owner_repo(execution,
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            package = fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'}, fixture, package, source)
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            observed = implementation_authoring.observe_candidate(fixture, facts)
            example = json.loads((SKILLS / 'packages/guru-check-task/examples/phase2-check.json').read_text())
            authored = {key:value for key,value in example.items() if key not in (
                'schema_version','skill_id','task_ref','phase2_capture_commit','reviewed_content_sha256')}
            authored.update(reviewed_paths=observed['reviewed_paths'], typed_exit='blocked',
                consumer={'kind':'stop','id':'task-check-blocked'}, reason='Original recorder transport fixture only.')
            authored['semantic_review'].update(status='blocked', summary='No native semantic result is asserted.')
            authored['delivery_policy'].update(task_scope=['R1'], delivery_slice=['R1'], remaining_work=[],
                current_slice_status='blocked', summary='Original recorder transport fixture only.')
            authored['docs_ssot'].update(status='blocked',durable_paths=['docs/range.md'],
                summary='No native Docs adequacy judgment is asserted.')
            before = repository_file_inventory(fixture)
            relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ),
                fixture.parent / 'check-recorder-receipts.json')
            input_locator = '.trellis/.runtime/guru-team/evals/phase2-owner-input.json'
            self.assertFalse((fixture / input_locator).exists())
            written = relay.forward({'skill_id':'implementation-authoring','command':'run','arguments':[],
                'stdin':json.dumps({'argv':[sys.executable,'-B','-c',
                    'import sys; from pathlib import Path; Path(sys.argv[1]).write_text(sys.argv[2])',
                    input_locator,json.dumps(authored)]})})
            self.assertEqual(json.loads(written['stdout'])['returncode'], 0)
            result = relay.forward({'skill_id':'guru-check-task','command':'record-phase2-check',
                'arguments':['--root',str(fixture),'--task',facts['task_ref'],'--input',input_locator],
                'stdin':''})
            self.assertEqual(result['returncode'],0,result['stderr'] or result['stdout'])
            receipt = json.loads(result['stdout'])
            self.assertFalse(receipt['formal_exit'])
            checkpoint = Path(receipt['result']['artifact_path']).relative_to(fixture.resolve()).as_posix()
            self.assertFalse(receipt['result']['dry_run'])
            cleaned = relay.forward({'skill_id':'implementation-authoring','command':'run','arguments':[],
                'stdin':json.dumps({'argv':[sys.executable,'-B','-c',
                    'import sys; from pathlib import Path; Path(sys.argv[1]).unlink()',input_locator]})})
            self.assertEqual(json.loads(cleaned['stdout'])['returncode'], 0)
            after = repository_file_inventory(fixture)
            changed = {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}
            self.assertEqual(changed,{checkpoint})
            self.assertIn(checkpoint,facts['owner_mutated_paths'])
            self.assertEqual(set(facts['owner_mutated_paths']),{facts['task_ref']+'/task.json',checkpoint,
                f".trellis/.runtime/guru-team/owner-checkpoints/{Path(facts['task_ref']).name}/{facts['delivery_key']['delivery_id']}/planning-approval.json"})
            for path in [*facts['writable_paths'],*facts['owner_mutated_paths']]:
                before.pop(path,None);after.pop(path,None)
            self.assertEqual(before,after)
            self.assertFalse(relay.terminal)

            # The native caller may use the original file-input Check entry.
            # Its final private transport consumes only that exact CLI file.
            projection=DeliveryProjection(fixture,facts['task_ref'])
            projection.begin_check(facts['delivery_key'],observed['candidate'])
            public=json.loads((fixture/'docs/phase2-evidence/check-public-input.json').read_text())
            public['source_exit']='implementation_complete'
            public_locator='.trellis/.runtime/guru-team/evals/phase2-public-input.json'
            written=relay.forward({'skill_id':'implementation-authoring','command':'run','arguments':[],
                'stdin':json.dumps({'argv':[sys.executable,'-B','-c',
                    'import sys; from pathlib import Path; Path(sys.argv[1]).write_text(sys.argv[2])',
                    public_locator,json.dumps(public)]})})
            self.assertEqual(json.loads(written['stdout'])['returncode'],0)
            checked=relay.forward({'skill_id':'guru-check-task','command':'check-phase2-check',
                'arguments':['--task',facts['task_ref']],'stdin':''})
            self.assertEqual(checked['returncode'],0,checked['stderr'] or checked['stdout'])
            intermediate=relay.forward({'skill_id':'guru-check-task','command':'invoke',
                'arguments':['--input',public_locator,'--owner-result',checkpoint],'stdin':''})
            self.assertEqual(intermediate['returncode'],0,intermediate['stderr'] or intermediate['stdout'])
            self.assertTrue((fixture/public_locator).is_file())
            self.assertFalse(relay.terminal)
            final=relay.forward({'skill_id':'guru-check-task','command':'invoke',
                'arguments':['--input='+str((fixture/public_locator).resolve()),'--owner-result',checkpoint],
                'stdin':json.dumps({'final':True,'invocation':{}})})
            self.assertEqual(final['returncode'],0,final['stderr'] or final['stdout'])
            self.assertEqual(final['stdout'],intermediate['stdout'])
            self.assertEqual(json.loads(final['stdout']),{'exit_id':'blocked'})
            self.assertEqual(relay.receipts[-1]['response'],final)
            self.assertFalse((fixture/public_locator).exists())
            self.assertTrue(relay.terminal)
            after=repository_file_inventory(fixture)
            for path in [*facts['writable_paths'],*facts['owner_mutated_paths']]:
                after.pop(path,None)
            self.assertEqual(before,after)

    def test_trace_binds_ordered_writable_versions_and_requires_initial_reads(self):
        # Real helper reads, writes, receipts and original wrapper stdout bind
        # the trace. This transport test makes no native semantic claim.
        from adapters.eval.test_native_constraint_transport import request as native_request
        for initial_reads_complete in (True,False):
            with self.subTest(initial_reads_complete=initial_reads_complete),tempfile.TemporaryDirectory() as temporary:
                request=native_request(Path(temporary),PACKAGE.name,'native-implementation-plan-premise')
                values=native_adapter.build_context(request,'codex')
                try:
                    protocol=json.loads(values[4].read_text())
                    repository=Path(protocol['repository_projection_root'])
                    facts_path=repository/implementation_authoring.FACTS
                    facts=json.loads(facts_path.read_text())
                    helper=[sys.executable,'-B',protocol['helper_path'],
                        '--trace',protocol['trace_path'],'--request-sha256',protocol['request_sha256'],
                        '--projection-root',protocol['projection_root'],'--repository-root',str(repository),
                        '--sandbox-root',protocol['model_root'],'--request-fifo',protocol['request_fifo'],
                        '--response-fifo',protocol['response_fifo'],'--skill-sha256',protocol['skill_sha256'],
                        '--wrapper-sha256',protocol['wrapper_sha256']]
                    def command(skill, name, stdin='', arguments=()):
                        result=subprocess.run([*helper,'command','--skill-id',skill,'--command',name,
                            '--stdin','--',*arguments],input=stdin,capture_output=True,text=True,check=False,timeout=20)
                        self.assertEqual(result.returncode,0,result.stderr or result.stdout)
                        return result.stdout
                    def read(path):
                        result=subprocess.run([*helper,'read','--kind','owner_file','--path',str(path)],
                            capture_output=True,text=True,check=False,timeout=20)
                        self.assertEqual(result.returncode,0,result.stderr)
                        return result.stdout
                    if not initial_reads_complete:
                        command('implementation-authoring','inspect')
                    for path in [facts_path,*[repository/relative for relative in facts['required_reads']]]:
                        read(path)
                    target=facts['planning_root']+'/prd.md'
                    seed=(repository/target).read_text()
                    versions=[seed+'\nTransport revision A.\n',seed+'\nTransport revision B.\n']
                    for content in versions:
                        command('implementation-authoring','write',json.dumps({'file_updates':{target:content}}))
                        self.assertEqual(read(repository/target),content)
                    public={'profile':'delivery_active_task_scope_change','mode':'workflow',
                        'task_ref':facts['task_ref'],'delivery_key':facts['delivery_key'],
                        'source_exit':'implementation_discovery','target_locator':'docs/implementation-observation.md',
                        'resume_target':'guru-resume-implementation','continuation_id':'trace-version-transport'}
                    owner={'public_input':public,'typed_exit':'blocked',
                        'reason':'Original wrapper transport only; no native semantic result is claimed.',
                        'ai_review_gate':{'status':'blocked','summary':'Deterministic trace transport test.'}}
                    stdout=command('guru-clarify-requirements','invoke',json.dumps({'final':True,
                        'invocation':{'public_input':public,'owner_result':owner}}),['--invocation','-'])
                    self.assertEqual(json.loads(stdout),{'exit_id':'blocked'})
                    if initial_reads_complete:
                        flags=native_adapter.validate_native_trace(Path(protocol['trace_path']),
                            protocol['request_sha256'],request,values[2],stdout,values[4])
                        self.assertIn('public_invocation',flags)
                    else:
                        with self.assertRaisesRegex(ValueError,'command preceded the supplied source'):
                            native_adapter.validate_native_trace(Path(protocol['trace_path']),
                                protocol['request_sha256'],request,values[2],stdout,values[4])
                finally:
                    values[9].set();values[8].join(timeout=2)

    def test_original_delivery_parse_error_can_be_corrected_through_same_fifo(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            fixture, source = stage_clean_installed_owner_repo(root / 'execution',
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            package = fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'}, fixture, package, source)
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            receipts = root / 'receipts.json'
            relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ), receipts)
            stop = threading.Event()
            request_fifo, response_fifo = root / 'request', root / 'response'
            thread = native_adapter.start_qualification_runtime_boundary(request_fifo, response_fifo,
                stop, fixture, package, dict(os.environ), {}, implementation_commands=relay)
            helper = root / 'helper.py'
            helper.write_text(qualification_trace_helper_source(allow_commands=True))
            trace = root / 'trace.json'
            argv = [sys.executable, '-B', str(helper), '--trace', str(trace),
                '--request-sha256', '1' * 64, '--projection-root', str(package),
                '--repository-root', str(fixture), '--sandbox-root', str(root),
                '--request-fifo', str(request_fifo), '--response-fifo', str(response_fifo),
                '--skill-sha256', '2' * 64, '--wrapper-sha256', '3' * 64, 'command']
            def call(skill, command, arguments=()):
                return subprocess.run([*argv, '--skill-id', skill, '--command=' + command, '--', *arguments],
                    input='', capture_output=True, text=True, check=False, timeout=20)
            try:
                bad = call('delivery-api', 'apply', ['apply', '--input', '{}'])
                self.assertEqual(bad.returncode, 2)
                self.assertIn('unrecognized arguments: apply', bad.stderr)
                self.assertFalse(relay.terminal)
                self.assertTrue(thread.is_alive())
                missing = call('delivery-api', 'apply')
                self.assertEqual(missing.returncode, 2)
                self.assertIn('delivery.py apply: error:', missing.stderr)
                self.assertFalse(relay.terminal)
                top_help = call('delivery-api', '--help')
                self.assertEqual(top_help.returncode, 0, top_help.stderr)
                help_result = call('delivery-api', 'apply', ['--help'])
                self.assertEqual(help_result.returncode, 0, help_result.stderr)
                self.assertIn('--input INPUT', help_result.stdout)
                contract = call('delivery-api', 'contract', ['--json'])
                self.assertEqual(json.loads(contract.stdout)['delivery_api'], '1.0')
                operation = {'api_version':'1.0', 'operation':'rework', 'key':facts['delivery_key'],
                    'owner_role':'implementation', 'owner_id':facts['declaration']['owners']['implementation'],
                    'expected_phase':'implementing', 'target_role':'planning',
                    'reason':DeliveryProjection(fixture,facts['task_ref']).resolve(facts['delivery_key'])['scope_ref']['authority'],
                    'affected_results':['planning','check','full_review','readiness']}
                corrected = call('delivery-api', 'apply', ['--task', facts['task_ref'], '--input', json.dumps(operation)])
                self.assertEqual(corrected.returncode, 0, corrected.stderr)
                self.assertEqual(DeliveryProjection(fixture,facts['task_ref']).resolve(facts['delivery_key'])['phase'], 'planning')
                wrapper_error = call(PACKAGE.name, 'invoke')
                self.assertNotEqual(wrapper_error.returncode, 0)
                thread.join(timeout=2)
                self.assertTrue(relay.terminal)
                self.assertFalse(thread.is_alive())
                rows = json.loads(receipts.read_text())
                self.assertEqual(rows[0]['request']['arguments'], ['apply', '--input', '{}'])
                self.assertEqual(rows[0]['response']['stderr'], bad.stderr)
                self.assertEqual([row['response']['returncode'] for row in rows[:6]], [2,2,0,0,0,0])
                self.assertEqual(len(json.loads(trace.read_text())['events']), len(rows))
                execution_relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ), root / 'execution-error.json')
                execution_error = execution_relay.forward({'skill_id':'delivery-api','command':'apply',
                    'arguments':['--task',facts['task_ref'],'--input','{}'],'stdin':''})
                self.assertEqual(execution_error['returncode'], 1)
                self.assertTrue(execution_relay.terminal)
            finally:
                stop.set()
                thread.join(timeout=2)

    def test_code_observation_records_actual_probe_without_a_design_verdict(self):
        with tempfile.TemporaryDirectory() as temporary:
            execution = Path(temporary) / 'execution'
            fixture, source = stage_clean_installed_owner_repo(
                execution, REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            package = fixture / '.trellis/guru-team/skills/packages/guru-check-task'
            implementation_authoring.stage({'case_id':'native-implementation-code-drift'}, fixture, package, source)
            text = (fixture / 'docs/implementation-observation.md').read_text()
            receipt = json.loads(text.split('```json\n',1)[1].split('\n```',1)[0])
            self.assertEqual(receipt['argv'][0], sys.executable)
            self.assertEqual(receipt['returncode'],0,receipt['stderr'])
            observed = json.loads(receipt['stdout'])
            self.assertEqual(observed['predicate'][2],{'input':[4,2,4],'output':False})
            self.assertEqual(observed['selection']['output'],[2,3])
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            first = implementation_authoring.observe_candidate(fixture, facts)
            relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ), fixture.parent / 'after-receipts.json')
            relay.forward({'skill_id':'implementation-authoring','command':'write','arguments':[],
                'stdin':json.dumps({'file_updates':{'interval.py':'def contains(value, lower, upper):\n    return lower <= value <= upper\n'}})})
            checked = relay.forward({'skill_id':'implementation-authoring','command':'run','arguments':[],
                'stdin':json.dumps({'argv':[sys.executable,'-B','-c',
                    'from range_filter import select; assert select([1,2,3,4,5],2,4)==[2,3,4]']})})
            self.assertEqual(json.loads(checked['stdout'])['returncode'],0)
            after = json.loads(relay.forward({'skill_id':'implementation-authoring','command':'inspect',
                'arguments':[],'stdin':''})['stdout'])
            self.assertNotEqual(after['candidate']['content_ref'],first['candidate']['content_ref'])
            self.assertNotEqual(after['reviewed_content_sha256'],first['reviewed_content_sha256'])
            self.assertIn('interval.py',after['candidate']['paths'])
            self.assertEqual(after['candidate']['base_ref'],first['fixed_base'])
            operation={'api_version':'1.0','operation':'begin_check','key':facts['delivery_key'],
                'owner_role':'implementation','owner_id':facts['declaration']['owners']['implementation'],
                'expected_phase':'implementing','candidate':after['candidate']}
            rebound=relay.forward({'skill_id':'delivery-api','command':'begin-check',
                'arguments':['--task',facts['task_ref'],'--input',json.dumps(operation)],'stdin':''})
            self.assertEqual(rebound['returncode'],0,rebound['stderr'])
            projection=DeliveryProjection(fixture,facts['task_ref'])
            self.assertEqual(projection.resolve(facts['delivery_key'])['candidate'],after['candidate'])
            self.assertEqual(projection.resolve(facts['delivery_key'])['phase'],'checking')
            self.assertEqual(after['current_head'],run_git(fixture,'rev-parse','HEAD'))

    def test_seed_and_original_rework_keep_same_delivery_and_scope(self):
        with tempfile.TemporaryDirectory() as temporary:
            execution = Path(temporary) / 'execution'
            fixture, source = stage_clean_installed_owner_repo(
                execution, REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            package = fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name
            implementation_authoring.stage({'case_id': 'native-implementation-plan-premise'}, fixture, package, source)
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            self.assertTrue(all((fixture / path).is_file() for path in facts['required_reads']))
            projection = DeliveryProjection(fixture, facts['task_ref'])
            before = projection.resolve(facts['delivery_key'])
            self.assertEqual(before['phase'], 'implementing')
            design = (fixture / facts['planning_root'] / 'design.md').read_text()
            self.assertIn('lower <= value < upper', design)
            self.assertIn('includes both endpoints', (fixture / 'docs/range.md').read_text())
            implementation = (fixture / 'interval.py').read_bytes()
            relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ), fixture.parent / 'command-receipts.json')
            written = relay.forward({'skill_id': 'implementation-authoring', 'command': 'write',
                'arguments': [], 'stdin': json.dumps({'file_updates': {'docs/operator-notes.md': '# Operator notes\n\nPure range evaluation performs no I/O.\n'}})})
            self.assertEqual(json.loads(written['stdout'])['written_paths'], ['docs/operator-notes.md'])
            operation = {'api_version': '1.0', 'operation': 'rework',
                'key': facts['delivery_key'], 'owner_role': 'implementation',
                'owner_id': facts['declaration']['owners']['implementation'],
                'expected_phase': 'implementing', 'target_role': 'planning',
                'reason': before['scope_ref']['authority'],
                'affected_results': ['planning', 'check', 'full_review', 'readiness']}
            result = relay.forward({'skill_id': 'delivery-api', 'command': 'rework',
                'arguments': ['--task', facts['task_ref'], '--input', json.dumps(operation)], 'stdin': ''})
            self.assertEqual(result['returncode'], 0, result['stderr'])
            after = projection.resolve(facts['delivery_key'])
            self.assertEqual(after['phase'], 'planning')
            self.assertEqual(before['scope_ref'], after['scope_ref'])
            self.assertEqual(before['id'], after['id'])
            self.assertEqual(implementation, (fixture / 'interval.py').read_bytes())
            selected = relay.forward({'skill_id': 'delivery-api', 'command': 'select',
                'arguments': ['--task', facts['task_ref'], '--delivery', facts['delivery_key']['delivery_id']], 'stdin': ''})
            self.assertEqual(selected['returncode'], 0, selected['stderr'])
            self.assertFalse(relay.terminal)
            self.assertEqual(len(json.loads((fixture.parent / 'command-receipts.json').read_text())), 3)
            author_public=json.loads((fixture/implementation_authoring.PUBLIC_INPUT).read_text())
            author_output={'exit_id':'requirements_ready','task_ref':facts['task_ref'],
                'delivery_key':facts['delivery_key'],'candidate':{'design_locator':facts['planning_root']+'/design.md'}}
            authored=relay.forward({'skill_id':'guru-author-task-plan','command':'invoke',
                'arguments':['--input',json.dumps(author_public),'--owner-result',json.dumps({
                    'public_input':author_public,'output':author_output,'ai_review_gate':{
                        'status':'passed','summary':'Objective C5 and original wrapper transport only.'}})],'stdin':''})
            self.assertEqual(authored['returncode'],0,authored['stderr'])
            self.assertEqual(json.loads(authored['stdout']),author_output)
            self.assertEqual(facts['task_checkout']['topology'],'linked')
            with self.assertRaisesRegex(ValueError,'fresh independent'):
                relay.forward({'skill_id':'guru-maintain-architecture-baseline','command':'invoke',
                    'arguments':['--invocation','-'],'stdin':'{}'})
            actual_blocked='{"exit_id":"blocked"}'
            requests=[]
            def review(value):
                requests.append(value)
                return {'returncode':0,'stdout':actual_blocked,'stderr':''}
            relay.independent_reviewer=review
            result=relay.forward({'skill_id':'guru-maintain-architecture-baseline','command':'independent-review',
                'arguments':[],'stdin':json.dumps({'public_input':{'stage':'planning'},'reads':['interval.py']})})
            self.assertEqual(result['stdout'],actual_blocked)
            self.assertEqual(requests,[{'public_input':{'stage':'planning'},'reads':['interval.py']}])
            self.assertFalse(relay.terminal)
            self.original_fresh_reviewer(fixture, facts, relay)
            public = {'profile': 'delivery_active_task_scope_change', 'mode': 'workflow',
                'task_ref': facts['task_ref'], 'delivery_key': facts['delivery_key'],
                'source_exit': 'implementation_discovery', 'target_locator': 'docs/implementation-observation.md',
                'resume_target': 'guru-resume-implementation', 'continuation_id': 'transport-only'}
            owner = {'public_input': public, 'typed_exit': 'blocked',
                'reason': 'Mechanical transport probe only; native judgment is separate.',
                'ai_review_gate': {'status': 'blocked', 'summary': 'Transport probe does not establish a semantic result.'}}
            stopped = relay.forward({'skill_id': 'guru-clarify-requirements', 'command': 'invoke',
                'arguments': ['--invocation', '-'], 'stdin': json.dumps({'final': True,
                    'invocation': {'public_input': public, 'owner_result': owner}})})
            self.assertEqual(stopped['returncode'], 0, stopped['stderr'])
            self.assertEqual(json.loads(stopped['stdout']), {'exit_id': 'blocked'})
            self.assertTrue(relay.terminal)

    def original_fresh_reviewer(self, fixture, facts, commands):
        # A new interpreter stands in for native inference only in this
        # deterministic transport test. It calls the actual original wrapper;
        # its owner fields are not supplied to any evaluated native Agent.
        root=fixture.parent/'reviewer-transport';root.mkdir()
        model=root/'model';model.mkdir();repository=model/'repository'
        stage_repository_projection(fixture,repository)
        (model/'native-context.txt').write_text('Overall implementation context.')
        private=root/'private';private.mkdir()
        worker=root/'worker.py'
        worker.write_text(textwrap.dedent('''\
            import hashlib,json,shlex,subprocess,sys
            from pathlib import Path
            context=sys.argv[-1]
            command=None
            for line in context.splitlines():
                if line.startswith('/') and ' read --kind ' in line:
                    if command is None:command=shlex.split(line.split(' read --kind ',1)[0])
                    result=subprocess.run(shlex.split(line),capture_output=True,text=True)
                    if result.returncode:raise SystemExit(result.stderr)
            locator=next(line.split(': ',1)[1] for line in context.splitlines() if line.startswith('Public input locator: '))
            public=json.loads(Path(locator).read_text())
            owner={key:public[key] for key in ('schema_version','profile','mode','continuation_id','stage',
                'task_locator','baseline','constitution','project_contract','freshness_identity',
                'planning_purpose','delivery_key','planning_root')}
            owner.update(input_sha256=hashlib.sha256(json.dumps(public,ensure_ascii=False,sort_keys=True,
                separators=(',',':')).encode()).hexdigest(),typed_exit='baseline_current',
                baseline_identity=public['baseline']['identity'],constitution_identity=public['constitution']['identity'],
                impact_kind='no_architecture_impact',impact_reason='Objective transport fixture only.',
                consumer={'kind':'workflow','id':'guru-architecture-baseline-current-router'},
                ai_review_gate={'status':'passed','reviewed_scope':'Objective transport fixture.',
                    'evidence_summary':'No native semantic judgment is claimed.','findings':[],
                    'conclusion':'Original wrapper transport only.'})
            result=subprocess.run([*command,'invoke','--stdin'],input=json.dumps({'public_input':public,
                'owner_result':owner}),capture_output=True,text=True)
            Path(sys.argv[sys.argv.index('--output-last-message')+1]).write_text(result.stdout)
            sys.stdout.write(result.stdout);sys.stderr.write(result.stderr)
            raise SystemExit(result.returncode)
            '''))
        package=fixture/'.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline'
        public=json.loads((package/'examples/public-input-delivery-task-impact-sync-1.0.json').read_text())
        public.update(task_locator=facts['task_ref'],delivery_key=facts['delivery_key'],
            planning_root=Path(facts['planning_root']).relative_to(facts['task_ref']).as_posix())
        public['baseline']['identity']='range-v1'
        public['constitution']['identity']='range-constitution-v1'
        public['project_contract'].update(change_contract_identity='range-contract-v1',
            required_concern_set_identity='range-concerns-v1')
        import hashlib
        public['freshness_identity']='sha256:'+hashlib.sha256(json.dumps(public['candidate'],
            ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        protocol={'repository_projection_root':str(repository),'model_root':str(model),
            'owner_repository':str(fixture),'private_root':str(private),'request_sha256':'a'*64}
        callback=native_adapter.implementation_reviewer(protocol,commands,
            [sys.executable,str(worker),'--ephemeral','--output-last-message',str(root/'unused'),'overall'],dict(os.environ))
        result=callback({'public_input':public,'reads':[
            'docs/architecture/00-foundation/design-constitution.md','docs/architecture/README.md',
            'docs/architecture/06-governance/change-contract.md',facts['planning_root']+'/design.md',
            'interval.py','range_filter.py','docs/range.md']})
        self.assertEqual(result['returncode'],0,result['stderr'])
        self.assertEqual(json.loads(result['stdout'])['exit_id'],'baseline_current')
        execution=json.loads((private/'implementation-architecture-executions.json').read_text())[0]
        trace=json.loads(Path(execution['trace_path']).read_text())
        self.assertEqual(sum(event['kind']=='invoke' for event in trace['events']),1)
        self.assertEqual((model/'native-context.txt').read_text(),'Overall implementation context.')

    def rdt_terminal_protocol(self, root, fixture, facts, *, revision_code='design_revision'):
        # Only deterministic transport is tested. These owner fields never
        # enter a native Agent and establish no semantic finding or approval.
        public = {'schema_version':'2.0','profile':'task_impact_sync',
            'source_exit':'implementation_complete','mode':'workflow','continuation_id':'continuation-transport',
            'stage':'phase2','task_locator':facts['task_ref'],'authority_locator':'docs/range.md',
            'authority_version':'range-rdt-v1',
            'authority_freshness':hashlib.sha256((fixture/'docs/range.md').read_bytes()).hexdigest(),
            'task_delta_locator':'docs/phase2-evidence/diff.patch','applicability_scope':'R1 range predicate/filter',
            'architecture_baseline':{'locator':'docs/architecture/README.md','version':'range-v1','status':'active'}}
        owner = {name:public[name] for name in ('profile','mode','continuation_id',
            'architecture_baseline','task_locator','authority_locator','authority_version')}
        owner.update(input_sha256=hashlib.sha256(json.dumps(public,ensure_ascii=False,
            sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            typed_exit='revision_required',revision_code=revision_code,affected_scope='R1 range design',
            consumer={'kind':'workflow','id':'guru-requirements-design-test-ssot-planning-router'},
            ai_review_gate={'status':'passed','reviewed_scope':'Original producer transport only.',
                'evidence_summary':'No native semantic finding is claimed.','findings':[],
                'conclusion':'Exercise the original output projection.'})
        receipts = root/'first-command-receipts.json'
        relay = implementation_authoring.ImplementationCommands(fixture,dict(os.environ),receipts)
        result = relay.forward({'skill_id':implementation_authoring.RDT,'command':'invoke',
            'arguments':['--invocation','-'],'stdin':json.dumps({'final':True,
                'invocation':{'public_input':public,'owner_result':owner}})})
        self.assertEqual(result['returncode'],0,result['stderr'] or result['stdout'])
        self.assertTrue(relay.terminal)
        request_path = root/'first-native-request.json'
        request_path.write_text(json.dumps({'case_id':'native-implementation-plan-premise'}))
        protocol_path = root/'first-native-protocol.json'
        protocol_path.write_text(json.dumps({'native_request_path':str(request_path),
            'owner_repository':str(fixture),'implementation_receipts_path':str(receipts),
            'implementation_context_id':'architecture-delivery-eval',
            'implementation_facts_locator':implementation_authoring.FACTS}))
        return protocol_path, result

    def test_planning_continuation_preserves_fixture_and_exports_actual_output(self):
        from runtime.reviewed_content import reviewed_content_identity
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            fixture,source=stage_clean_installed_owner_repo(root/'execution',
                REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh',PACKAGE)
            fixture=fixture.resolve()
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'},fixture,
                fixture/'.trellis/guru-team/skills/packages'/PACKAGE.name,source)
            facts=json.loads((fixture/implementation_authoring.FACTS).read_text())
            protocol,result=self.rdt_terminal_protocol(root,fixture,facts)
            raw_before={path:path.read_bytes() for path in (protocol,root/'first-command-receipts.json',
                root/'first-native-request.json')}
            before=repository_file_inventory(fixture)
            candidate_before=reviewed_content_identity(fixture)
            request={'case_id':'native-implementation-plan-premise','skill_id':PACKAGE.name,
                     'package_root':str(PACKAGE)}
            with patch.dict(os.environ,{implementation_authoring.PLANNING_CONTINUATION_PROTOCOL_ENV:str(protocol)}):
                package,dispatcher,environment=implementation_authoring.planning_continuation_execution(request)
                self.assertEqual(implementation_authoring.facts_locator(request),
                    implementation_authoring.PLANNING_CONTINUATION_FACTS)
            self.assertEqual(package,fixture/'.trellis/guru-team/skills/packages'/PACKAGE.name)
            self.assertTrue(dispatcher.is_file())
            self.assertEqual(environment,{'TRELLIS_CONTEXT_ID':'architecture-delivery-eval'})
            continuation=json.loads((fixture/implementation_authoring.PLANNING_CONTINUATION_FACTS).read_text())
            locator=continuation['public_input_locator']
            public=json.loads((fixture/locator).read_text())
            self.assertEqual(public['preceding_output'],json.loads(result['stdout']))
            self.assertEqual(public['current']['key'],facts['delivery_key'])
            self.assertEqual(public['delivery'],DeliveryProjection(fixture,facts['task_ref']).resolve(facts['delivery_key']))
            self.assertIn(locator,continuation['required_reads'])
            self.assertIn(implementation_authoring.PUBLIC_INPUT,continuation['required_reads'])
            after=repository_file_inventory(fixture)
            changed={path for path in before.keys()|after.keys() if before.get(path)!=after.get(path)}
            self.assertEqual(changed,{locator,implementation_authoring.PLANNING_CONTINUATION_FACTS})
            self.assertEqual(reviewed_content_identity(fixture),candidate_before)
            self.assertTrue(all(path.read_bytes()==content for path,content in raw_before.items()))

    def test_planning_continuation_rejects_other_original_revision_and_released_selection(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            fixture,source=stage_clean_installed_owner_repo(root/'execution',
                REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh',PACKAGE)
            fixture=fixture.resolve()
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'},fixture,
                fixture/'.trellis/guru-team/skills/packages'/PACKAGE.name,source)
            facts=json.loads((fixture/implementation_authoring.FACTS).read_text())
            request={'case_id':'native-implementation-plan-premise','skill_id':PACKAGE.name,
                     'package_root':str(PACKAGE)}
            other=root/'other';other.mkdir()
            protocol,_=self.rdt_terminal_protocol(other,fixture,facts,revision_code='test_revision')
            before=repository_file_inventory(fixture)
            with patch.dict(os.environ,{implementation_authoring.PLANNING_CONTINUATION_PROTOCOL_ENV:str(protocol)}):
                with self.assertRaisesRegex(ValueError,'terminal RDT design_revision'):
                    implementation_authoring.planning_continuation_execution(request)
            self.assertEqual(repository_file_inventory(fixture),before)
            protocol,_=self.rdt_terminal_protocol(root,fixture,facts)
            with patch.dict(os.environ,{'TRELLIS_CONTEXT_ID':'architecture-delivery-eval'}):
                projection=DeliveryProjection(fixture,facts['task_ref'])
                self.assertEqual(projection.current()['key'],facts['delivery_key'])
                projection.release(facts['delivery_key'])
                self.assertNotEqual(projection.current().get('kind'),'current')
            before=repository_file_inventory(fixture)
            with patch.dict(os.environ,{implementation_authoring.PLANNING_CONTINUATION_PROTOCOL_ENV:str(protocol)}):
                with self.assertRaisesRegex(ValueError,'same current Task and Delivery'):
                    implementation_authoring.planning_continuation_execution(request)
            self.assertEqual(repository_file_inventory(fixture),before)

    def test_planning_continuation_context_protocol_can_feed_strict_activation_resume(self):
        # Native inference is not executed. Original wrappers supply actual
        # producer stdout; build_context supplies the real private protocol.
        from adapters.eval.test_native_constraint_transport import request as native_request
        from runtime.delivery_projection.gates import rework
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            fixture,source=stage_clean_installed_owner_repo(root/'first',
                REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh',PACKAGE)
            fixture=fixture.resolve()
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'},fixture,
                fixture/'.trellis/guru-team/skills/packages'/PACKAGE.name,source)
            facts=json.loads((fixture/implementation_authoring.FACTS).read_text())
            first_facts=(fixture/implementation_authoring.FACTS).read_bytes()
            protocol,_=self.rdt_terminal_protocol(root,fixture,facts)
            request=native_request(root/'continuation',PACKAGE.name,'native-implementation-plan-premise')
            with patch.dict(os.environ,{implementation_authoring.PLANNING_CONTINUATION_PROTOCOL_ENV:str(protocol)}):
                with patch.object(native_adapter,'stage_owner_execution',side_effect=AssertionError('must reuse fixture')):
                    values=native_adapter.build_context(request,'codex')
            try:
                own_protocol=json.loads(values[4].read_text())
                self.assertEqual(Path(own_protocol['owner_repository']),fixture)
                self.assertEqual(own_protocol['implementation_facts_locator'],
                    implementation_authoring.PLANNING_CONTINUATION_FACTS)
                projected=Path(own_protocol['repository_projection_root'])
                continuation=json.loads((projected/implementation_authoring.PLANNING_CONTINUATION_FACTS).read_text())
                self.assertTrue(all((projected/path).is_file() for path in continuation['required_reads']))
                self.assertIsNone(own_protocol['architecture_context'])
                self.assertTrue(own_protocol['implementation_commands'])
                self.assertIn(str(projected/continuation['public_input_locator']),values[0])
            finally:
                values[9].set();values[8].join(timeout=2)
            projection=DeliveryProjection(fixture,facts['task_ref']);key=facts['delivery_key']
            rework(projection,key,'implementation','planning',projection.resolve(key)['scope_ref']['authority'],
                ['planning','check','full_review','readiness'])
            public={'profile':'delivery_initial_review','mode':'workflow','task_ref':facts['task_ref'],
                'delivery_key':key,'source_exit':'baseline_current',
                'architecture_assessment':delivery_production.final_architecture(
                    fixture,fixture/facts['task_ref'],key,preserve_existing_constitution=True)}
            authored=json.loads((SKILLS/'packages/guru-approve-task-plan/examples/planning-approval-delivery.json').read_text())
            authored={name:authored[name] for name in ('mode','authority_refs','delivery_policy',
                'docs_ssot_plan','semantic_review','typed_exit','consumer','reason')}
            authored['authority_refs']=['docs/range.md']
            authored['delivery_policy'].update(task_scope=['R1'],delivery_slice=['R1'],remaining_work=[],
                remaining_work_owner='No deferred scope in this deterministic transport fixture.')
            authored['docs_ssot_plan'].update(durable_paths=['docs/range.md'],
                summary='Actual original recorder transport, without native semantic approval.')
            authored['semantic_review']['summary']='Original wrapper transport only.'
            path=root/'approval-input.json';path.write_text(json.dumps(authored))
            relay=implementation_authoring.ImplementationCommands(fixture,dict(os.environ),
                Path(own_protocol['implementation_receipts_path']),
                facts_relative=implementation_authoring.PLANNING_CONTINUATION_FACTS)
            recorded=relay.forward({'skill_id':'guru-approve-task-plan','command':'record-planning-approval',
                'arguments':['--task',facts['task_ref'],'--delivery-key',json.dumps(key),'--input',str(path)],'stdin':''})
            self.assertEqual(recorded['returncode'],0,recorded['stderr'] or recorded['stdout'])
            checkpoint=json.loads(recorded['stdout'])['result']['artifact_path']
            checked=relay.forward({'skill_id':'guru-approve-task-plan','command':'check-planning-approval',
                'arguments':['--task',facts['task_ref'],'--delivery-key',json.dumps(key),
                    '--require-exit','approved'],'stdin':''})
            self.assertEqual(checked['returncode'],0,checked['stderr'] or checked['stdout'])
            owner=json.loads(Path(checkpoint).read_text())
            approved=relay.forward({'skill_id':'guru-approve-task-plan','command':'invoke',
                'arguments':['--invocation','-'],'stdin':json.dumps({'final':True,
                    'invocation':{'public_input':public,'owner_result':owner}})})
            self.assertEqual(approved['returncode'],0,approved['stderr'] or approved['stdout'])
            approved=json.loads(approved['stdout']);self.assertEqual(approved['exit_id'],'approved')
            activation_runtime=load_package_runtime_module(fixture/'.trellis/guru-team/scripts/bash/run-skill-command.sh',
                'guru-activate-delivery','invoke')
            activation=activation_runtime.invoke(fixture/'.trellis/guru-team/skills/packages/guru-activate-delivery',fixture,
                {**{name:approved[name] for name in ('task_ref','delivery_key','planning_result_id')},
                 'profile':'delivery_activation','mode':'workflow','action':'activate'},
                {'typed_exit':'delivery_started','reason':'Original activation for transport regression only.'})
            output=root/'activation-output.json';output.write_text(json.dumps(activation))
            resume_request=native_request(root/'resume',PACKAGE.name,implementation_authoring.RESUME_CASE)
            with patch.dict(os.environ,{implementation_authoring.RESUME_PROTOCOL_ENV:str(values[4]),
                    implementation_authoring.ACTIVATION_OUTPUT_ENV:str(output)}):
                with patch.object(native_adapter,'stage_owner_execution',side_effect=AssertionError('must reuse fixture')):
                    resumed=native_adapter.build_context(resume_request,'codex')
            try:
                resume_protocol=json.loads(resumed[4].read_text())
                self.assertEqual(Path(resume_protocol['owner_repository']),fixture)
                self.assertEqual(resume_protocol['implementation_facts_locator'],implementation_authoring.RESUME_FACTS)
                projected=Path(resume_protocol['repository_projection_root'])
                resume_facts=json.loads((projected/implementation_authoring.RESUME_FACTS).read_text())
                self.assertTrue(all((projected/path).is_file() for path in resume_facts['required_reads']))
                current=json.loads((projected/'docs/implementation-continuation-public.json').read_text())
                self.assertEqual(current['activation_output'],activation)
                self.assertEqual(current['current']['key'],key)
                self.assertEqual(current['delivery']['phase'],'implementing')
                self.assertIsNone(resume_protocol['architecture_context'])
                self.assertTrue(resume_protocol['implementation_commands'])
            finally:
                resumed[9].set();resumed[8].join(timeout=2)
            self.assertEqual((fixture/implementation_authoring.FACTS).read_bytes(),first_facts)

    def test_resume_uses_same_fixture_and_original_activation_without_changing_first_facts(self):
        # The first-segment receipt is a transport double for this unit test.
        # It is never staged for a native Agent and proves no semantic approval.
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            fixture,source=stage_clean_installed_owner_repo(root/'execution',
                REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh',PACKAGE)
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'},fixture,
                fixture/'.trellis/guru-team/skills/packages'/PACKAGE.name,source)
            facts_path=fixture/implementation_authoring.FACTS
            before=facts_path.read_bytes();facts=json.loads(before)
            authority_before=(fixture/'docs/range.md').read_bytes()
            activation_package=fixture/'.trellis/guru-team/skills/packages/guru-activate-delivery'
            module=load_package_runtime_module(fixture/'.trellis/guru-team/scripts/bash/run-skill-command.sh',
                'guru-activate-delivery','invoke')
            directory=DeliveryProjection(fixture,facts['task_ref']).planning_directory(facts['delivery_key'])
            approved={'exit_id':'approved','task_ref':facts['task_ref'],'delivery_key':facts['delivery_key'],
                'planning_result_id':module.planning_identity(fixture,directory)}
            activation=module.invoke(activation_package,fixture,
                {**{k:approved[k] for k in ('task_ref','delivery_key','planning_result_id')},
                 'profile':'delivery_activation','mode':'workflow','action':'recover_activation'},
                {'typed_exit':'delivery_started','reason':'Objective same-fixture recovery transport test.'})
            self.assertEqual(activation['exit_id'],'delivery_started')
            first_request=root/'first-native-request.json';first_request.write_text(json.dumps(
                {'case_id':'native-implementation-plan-premise'}))
            receipts=root/'receipts.json';receipts.write_text(json.dumps([{
                'request':{'skill_id':'guru-approve-task-plan','command':'invoke'},
                'response':{'returncode':0,'stdout':json.dumps(approved)}}]))
            protocol=root/'first-protocol.json';protocol.write_text(json.dumps({
                'native_request_path':str(first_request),'owner_repository':str(fixture),
                'implementation_receipts_path':str(receipts)}))
            output=root/'activation-output.json';output.write_text(json.dumps(activation))
            request={'skill_id':PACKAGE.name,'case_id':implementation_authoring.RESUME_CASE,
                     'package_root':str(PACKAGE)}
            with patch.dict(os.environ,{implementation_authoring.RESUME_PROTOCOL_ENV:str(protocol),
                                        implementation_authoring.ACTIVATION_OUTPUT_ENV:str(output)}):
                package,dispatcher,environment=implementation_authoring.resume_execution(request)
                self.assertEqual(package,(fixture/'.trellis/guru-team/skills/packages'/PACKAGE.name).resolve())
                self.assertTrue(dispatcher.is_file())
                self.assertEqual(facts_path.read_bytes(),before)
                self.assertEqual((fixture/'docs/range.md').read_bytes(),authority_before)
                continuation=json.loads((fixture/implementation_authoring.RESUME_FACTS).read_text())
                self.assertEqual(continuation['current_delivery']['phase'],'implementing')
                self.assertIn('docs/implementation-continuation-public.json',continuation['required_reads'])
                from runtime.delivery_projection.gates import rework
                projection=DeliveryProjection(fixture,facts['task_ref'])
                rework(projection,facts['delivery_key'],'implementation','planning',
                    projection.resolve(facts['delivery_key'])['scope_ref']['authority'],
                    ['planning','check','full_review','readiness'])
                with self.assertRaisesRegex(ValueError,'matching current Activation'):
                    implementation_authoring.resume_execution(request)


if __name__ == '__main__':
    unittest.main()
