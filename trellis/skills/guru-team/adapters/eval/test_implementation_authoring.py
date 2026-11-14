from __future__ import annotations

import json
import hashlib
import ast
import os
import shlex
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import threading
import unittest
import tomllib
from contextlib import ExitStack
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from adapters.eval import architecture_authoring, delivery_production, implementation_authoring, native_adapter, phase2_authoring
from adapters.eval.eval_support import qualification_trace_helper_source, stage_repository_projection, repository_file_inventory
from adapters.eval.fixture_io import stage_clean_installed_owner_repo, run_git
from runtime.delivery_projection.adapter import DeliveryProjection
from adapters.eval.owner_runtime import load_package_runtime_module

SKILLS = Path(__file__).resolve().parents[2]
REPO = SKILLS.parents[2]
PACKAGE = SKILLS / 'packages/guru-author-task-plan'


class ImplementationAuthoringTests(unittest.TestCase):
    def snapshot_transport_context(self, request):
        # This test's boundary is command/read transport over an existing
        # Planning snapshot. It is not the new no-Task native entry.
        with patch.object(implementation_authoring, 'initial_request_entry', return_value=False), \
                patch.object(implementation_authoring, 'stage', implementation_authoring.stage_planning_snapshot):
            return native_adapter.build_context(request, 'codex')

    def stage_historical_fixture(self, request, fixture, package, source):
        """Module transport precondition through real original producers.

        This setup is not supplied to a native Agent and establishes no native
        semantic proof. Business bytes and original result assertions stay real.
        """
        original = phase2_authoring.stage
        def historical_setup(*args, **kwargs):
            kwargs['fact_only'] = False
            return original(*args, **kwargs)
        with patch.object(phase2_authoring, 'stage', side_effect=historical_setup):
            implementation_authoring.stage(request, fixture, package, source)
        facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
        projection = DeliveryProjection(fixture, facts['task_ref'])
        key = facts['delivery_key']
        before = projection.resolve(key)
        self.assertEqual(before['phase'], 'checking')
        self.assertIsNotNone(before['results']['planning'])
        from runtime.delivery_projection.gates import rework
        rework(projection, key, 'check', 'implementation', before['scope_ref']['authority'],
               ['check', 'full_review', 'readiness'])
        after = projection.resolve(key)
        self.assertEqual(after['results']['planning'], before['results']['planning'])
        self.assertEqual(after['candidate'], before['candidate'])
        self.assertEqual(after['scope_ref'], before['scope_ref'])
        facts.update(current_delivery=after, current_selection=projection.current(key),
            seed_boundary='Historical module transport precondition from original producers; no native judgment is claimed.')
        (fixture / implementation_authoring.FACTS).write_text(json.dumps(facts, indent=2) + '\n')
        public = {'profile':'delivery_initial_review', 'mode':'workflow',
            'task_ref':facts['task_ref'], 'delivery_key':key,
            'source_selection':[{'locator':'docs/range.md', 'section':'Integer Range', 'authority_kind':'requirement'}]}
        if request['case_id'] == 'native-implementation-code-drift':
            public = json.loads((fixture / 'docs/phase2-evidence/check-public-input.json').read_text())
        (fixture / implementation_authoring.PUBLIC_INPUT).write_text(json.dumps(public) + '\n')

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
        self.assertFalse(relay.terminal)
        stop = threading.Event()
        request_fifo = fixture.parent / 'terminal-request'
        response_fifo = fixture.parent / 'terminal-response'
        thread = native_adapter.start_qualification_runtime_boundary(
            request_fifo, response_fifo, stop, fixture,
            fixture / '.trellis/guru-team/skills/packages' / implementation_authoring.RDT,
            {}, {}, implementation_commands=relay)
        client = ('import json,sys; from pathlib import Path; '
            'payload=sys.stdin.read(); '
            'Path(sys.argv[1]).write_text(payload); '
            'print(Path(sys.argv[2]).read_text())')
        malformed = {'skill_id':implementation_authoring.RDT,'command':'unknown-command',
                     'arguments':[],'stdin':''}
        diagnosis = {'skill_id':'implementation-authoring','command':'run','arguments':[],
            'stdin':json.dumps({'argv':['git','rev-parse','HEAD']})}
        try:
            for request in (malformed, diagnosis):
                response = subprocess.run([sys.executable, '-c', client,
                    str(request_fifo), str(response_fifo)], input=json.dumps(request),
                    capture_output=True, text=True, check=True, timeout=5)
                actual = json.loads(response.stdout)
                if request is malformed:
                    self.assertEqual(actual['returncode'], 2)
                    self.assertIn('not declared', actual['stderr'])
                else:
                    self.assertEqual(actual['returncode'], 0)
                    process = json.loads(actual['stdout'])
                    self.assertEqual(process['returncode'], 0)
                    self.assertEqual(process['stdout'].strip(), run_git(fixture, 'rev-parse', 'HEAD'))
                self.assertFalse(relay.terminal)
        finally:
            stop.set()
            thread.join(timeout=2)
        prefix = '.trellis/guru-team/skills/packages/' + implementation_authoring.RDT + '/'
        for relative in ('SKILL.md','interface.json','commands.json','references/contract.md',
                'references/current-knowledge.md'):
            self.assertTrue((fixture / (prefix + relative)).is_file())

    def test_native_planning_seed_preserves_business_and_has_no_stage_results(self):
        for case_id, test_names in (
                ('native-implementation-plan-premise', {'test_lower_and_interior','test_upper_and_singleton','test_outside'}),
                ('native-implementation-authority-conflict', {'test_endpoints_and_interior','test_outside','test_singleton','test_negative'}),
                ('native-implementation-code-drift', {'test_endpoints_and_interior','test_outside','test_singleton','test_negative'})):
            with self.subTest(case_id=case_id), tempfile.TemporaryDirectory() as temporary:
                fixture, source = stage_clean_installed_owner_repo(Path(temporary) / 'execution',
                    REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
                fixture = fixture.resolve()
                original_identity = architecture_authoring.stage_delivery_identity
                captured = {}
                def capture_identity(repository, public, **options):
                    captured['authority_before_scope'] = (repository / 'docs/range.md').read_bytes()
                    return original_identity(repository, public, **options)
                with patch.object(architecture_authoring, 'stage_delivery_identity', side_effect=capture_identity), \
                        patch.object(delivery_production, 'activate', wraps=delivery_production.activate) as activation:
                    implementation_authoring.stage({'case_id':case_id}, fixture,
                        fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name, source)
                activation.assert_not_called()
                facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
                projection = DeliveryProjection(fixture, facts['task_ref'])
                current = projection.resolve(facts['delivery_key'])
                self.assertEqual(current['phase'], 'planning')
                self.assertIsNone(current['candidate'])
                self.assertIsNone(current['plan_ref'])
                self.assertTrue(all(value is None for value in current['results'].values()))
                self.assertEqual((fixture / 'docs/range.md').read_bytes(), captured['authority_before_scope'])
                self.assertNotIn('profile', json.loads((fixture / implementation_authoring.PUBLIC_INPUT).read_text()))
                self.assertNotIn('planning_candidate_syntax', facts)
                self.assertNotIn('execution_surface', facts)
                self.assertFalse((fixture / phase2_authoring.ARCHITECTURE_INPUT).exists())
                self.assertFalse((fixture / 'docs/phase2-evidence/check-public-input.json').exists())
                tree = ast.parse((fixture / 'test_interval.py').read_bytes())
                actual = {node.name for node in ast.walk(tree)
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}
                self.assertEqual(actual, test_names)
                design = (fixture / facts['planning_root'] / 'design.md').read_text()
                validation = json.loads((fixture / 'docs/phase2-evidence/validation.json').read_text())
                if case_id == 'native-implementation-plan-premise':
                    self.assertIn('lower <= value < upper', design)
                    self.assertEqual(validation['returncode'], 0, validation['stderr'])
                    self.assertIn('self.assertFalse(contains(4, 2, 4))', (fixture / 'test_interval.py').read_text())
                else:
                    self.assertIn('integer comparisons' if case_id.endswith('authority-conflict') else 'lower <= value <= upper', design)
                    self.assertNotEqual(validation['returncode'], 0)
                self.assertIn('includes both endpoints', (fixture / 'docs/range.md').read_text())
                self.assertIn('interval.py owns a pure predicate', (fixture / 'docs/architecture/README.md').read_text())
                self.assert_rdt_command_reaches_original_wrapper(fixture, facts)

    def test_inspect_original_error_then_caller_selected_baseline(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture, source = stage_clean_installed_owner_repo(Path(temporary) / 'execution',
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            fixture = fixture.resolve()
            implementation_authoring.stage({'case_id':'native-implementation-plan-premise'}, fixture,
                fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name, source)
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            projection = DeliveryProjection(fixture, facts['task_ref'])
            before = projection.resolve(facts['delivery_key'])
            self.assertIsNone(before['candidate'])
            relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ),
                fixture.parent / 'inspect-receipts.json')
            paths = ['interval.py', 'test_interval.py']
            payload = {'skill_id':'implementation-authoring','command':'inspect','arguments':[],
                       'stdin':json.dumps({'paths':paths})}
            failed = relay.forward(payload)
            original = subprocess.run(['bash', '.trellis/guru-team/scripts/bash/construct-delivery-candidate.sh',
                '--root', '.', '--task', facts['task_ref'], '--delivery-key', json.dumps(facts['delivery_key']),
                '--head', run_git(fixture, 'rev-parse', 'HEAD'), '--paths', *paths],
                cwd=fixture, capture_output=True, text=True, check=False)
            self.assertEqual(failed, {'returncode':original.returncode,
                'stdout':original.stdout,'stderr':original.stderr})
            self.assertNotEqual(failed['returncode'], 0)
            self.assertEqual(json.loads(failed['stdout'])['code'], 'candidate_commit_missing')
            self.assertFalse(relay.terminal)
            baseline = run_git(fixture, 'rev-parse', 'HEAD')
            for field in ('development_base', 'observed_target'):
                corrected = relay.forward({**payload,'stdin':json.dumps({'paths':paths,field:baseline})})
                self.assertEqual(corrected['returncode'], 0, corrected)
                self.assertEqual(json.loads(corrected['stdout'])['candidate']['base_ref'], baseline)
                self.assertFalse(relay.terminal)
                self.assertEqual(projection.resolve(facts['delivery_key']), before)

    def test_original_approval_commands_change_only_current_delivery_checkpoint(self):
        # This executes deterministic owner transport, not native inference.
        with tempfile.TemporaryDirectory() as temporary:
            fixture, source = stage_clean_installed_owner_repo(Path(temporary) / 'execution',
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            fixture = fixture.resolve()
            self.stage_historical_fixture({'case_id':'native-implementation-plan-premise'}, fixture,
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
                self.stage_historical_fixture({'case_id':'native-implementation-code-drift'}, fixture,
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
            self.stage_historical_fixture({'case_id':'native-implementation-plan-premise'}, fixture, package, source)
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            observed = implementation_authoring.observe_candidate(fixture, facts)
            reviewed_paths = sorted({*observed['reviewed_paths'],
                *run_git(fixture, 'diff', '--name-only').splitlines(),
                *run_git(fixture, 'ls-files', '--others', '--exclude-standard').splitlines()})
            authored = json.loads((SKILLS / 'packages/guru-check-task/examples/phase2-authoring.json').read_text())
            authored.update(reviewed_paths=reviewed_paths, typed_exit='blocked',
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
            from adapters.eval.stage_result_authoring import ImplementationCommands as StageCommands
            stage_relay = StageCommands(fixture, dict(os.environ),
                fixture.parent / 'stage-check-recorder-receipts.json',
                facts_relative=implementation_authoring.FACTS)
            result = stage_relay.forward({'skill_id':'guru-check-task','command':'record-phase2-check',
                'arguments':['--root',str(fixture),'--task',facts['task_ref'],'--input',input_locator],
                'stdin':''})
            self.assertEqual(result['returncode'],0,result['stderr'] or result['stdout'])
            self.assertFalse((fixture / input_locator).exists())
            self.assertIn(input_locator, stage_relay.consumed_paths)
            receipt = json.loads(result['stdout'])
            self.assertFalse(receipt['formal_exit'])
            checkpoint = Path(receipt['result']['artifact_path']).relative_to(fixture.resolve()).as_posix()
            self.assertFalse(receipt['result']['dry_run'])
            from adapters.eval.stage_result_authoring import additional_mutated_paths
            self.assertIn(checkpoint, additional_mutated_paths(fixture,
                {**facts, 'continuous_chain': True}))
            source_file = fixture / 'interval.py'
            source_before = source_file.read_text()
            source_revision = source_before + '\n# Ordinary source revision after capture.\n'
            def source_write(content):
                changed = stage_relay.forward({'skill_id':'implementation-authoring','command':'run',
                    'arguments':[], 'stdin':json.dumps({'argv':[sys.executable,'-B','-c',
                        'import sys; from pathlib import Path; Path("interval.py").write_text(sys.argv[1])',
                        content]})})
                self.assertEqual(json.loads(changed['stdout'])['returncode'], 0)
            source_write(source_revision)
            stale_index = len(stage_relay.receipts)
            stale = stage_relay.forward({'skill_id':'guru-check-task','command':'check-phase2-check',
                'arguments':['--task',facts['task_ref']], 'stdin':''})
            self.assertEqual(stale['returncode'], 3)
            self.assertEqual(json.loads(stale['stdout'])['code'], 'stale_identity')
            self.assertFalse(stage_relay.terminal)
            diagnostic = stage_relay.forward({'skill_id':'implementation-authoring','command':'run',
                'arguments':[], 'stdin':json.dumps({'argv':[sys.executable,'-B','-c',
                    'from pathlib import Path; print(Path("interval.py").read_text(), end="")']})})
            self.assertEqual(json.loads(diagnostic['stdout'])['stdout'], source_revision)
            source_write(source_before)
            (fixture / input_locator).write_text(json.dumps(authored))
            refreshed = stage_relay.forward({'skill_id':'guru-check-task','command':'record-phase2-check',
                'arguments':['--task',facts['task_ref'],'--input',input_locator], 'stdin':''})
            self.assertEqual(refreshed['returncode'], 0, refreshed['stdout'])
            checked = stage_relay.forward({'skill_id':'guru-check-task','command':'check-phase2-check',
                'arguments':['--task',facts['task_ref']], 'stdin':''})
            self.assertEqual(checked['returncode'], 0, checked['stdout'])
            self.assertEqual(stage_relay.receipts[stale_index]['response'], stale)
            self.assertFalse(stage_relay.terminal)
            self.assertFalse((fixture / input_locator).exists())
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

    def test_documented_transport_sends_stdin_and_runs_in_owner_checkout(self):
        # Execute the shell example from the actual model context. This proves
        # transport syntax and checkout mapping, not native owner judgment.
        from adapters.eval.test_native_constraint_transport import request as native_request
        with tempfile.TemporaryDirectory() as temporary:
            request = native_request(Path(temporary), PACKAGE.name, 'native-implementation-plan-premise')
            values = self.snapshot_transport_context(request)
            try:
                protocol = json.loads(values[4].read_text())
                repository = Path(protocol['repository_projection_root'])
                owner = Path(protocol['owner_repository'])
                facts = json.loads((repository / implementation_authoring.FACTS).read_text())
                context = (Path(protocol['model_root']) / 'native-context.txt').read_text()
                examples = [block.split('```', 1)[0] for block in context.split('```bash\n')[1:]]
                example = next((block for block in examples if '<current-command-input-json>' in block), None)
                self.assertIsNotNone(example, 'R5 context must supply its executable stdin example')
                target = facts['planning_root'] + '/prd.md'
                content = (owner / target).read_text() + '\nTransport preserves $HOME and `literal` bytes.\n'

                def documented_command(skill, command, payload, arguments=()):
                    script = (example.replace('<skill>', skill).replace('<command>', command)
                        .replace('<original arguments>', shlex.join(arguments))
                        .replace('<current-command-input-json>', json.dumps(payload)))
                    return subprocess.run(['bash', '-c', script], cwd=protocol['model_root'],
                        capture_output=True, text=True, check=False, timeout=20)

                written = documented_command('implementation-authoring', 'write',
                    {'file_updates': {target: content}})
                self.assertEqual(written.returncode, 0, written.stderr)
                self.assertEqual(json.loads(written.stdout)['written_paths'], [target])
                self.assertEqual((owner / target).read_text(), content)
                # Reads use a non-Git projection; commands use the original Git
                # checkout. A model-visible absolute path is not the command cwd.
                self.assertFalse((repository / '.git').exists())
                observed = documented_command('implementation-authoring', 'run',
                    {'argv': ['git', '-C', '.', 'rev-parse', '--show-toplevel']})
                self.assertEqual(observed.returncode, 0, observed.stderr)
                process = json.loads(observed.stdout)
                self.assertEqual(process['returncode'], 0, process['stderr'])
                self.assertEqual(Path(process['stdout'].strip()).resolve(), owner.resolve())
                receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
                self.assertEqual(json.loads(receipts[0]['request']['stdin']), {'file_updates': {target: content}})
                trace = json.loads(Path(protocol['trace_path']).read_text())
                events = [row for row in trace['events'] if row['kind'] == 'command']
                self.assertEqual(len(events), len(receipts))
            finally:
                values[9].set()
                values[8].join(timeout=2)

    def test_trace_binds_ordered_writable_versions_and_requires_initial_reads(self):
        # Real helper reads, writes, receipts and original wrapper stdout bind
        # the trace. This transport test makes no native semantic claim.
        from adapters.eval.test_native_constraint_transport import request as native_request
        for initial_reads_complete,defer_owner_reads in ((True,False),(True,True),(False,False)):
            with self.subTest(initial_reads_complete=initial_reads_complete,defer_owner_reads=defer_owner_reads),tempfile.TemporaryDirectory() as temporary:
                request=native_request(Path(temporary),PACKAGE.name,'native-implementation-plan-premise')
                values=self.snapshot_transport_context(request)
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
                        command('implementation-authoring', 'run', json.dumps({
                            'argv': [sys.executable, '-B', '-c', 'print("transport read-order probe")']}))
                    for path in [facts_path,*[repository/relative for relative in facts['required_reads']]]:
                        if defer_owner_reads and path.is_relative_to(repository/'.trellis/guru-team/skills/packages'):
                            continue
                        read(path)
                    if defer_owner_reads:
                        # The first public fact query needs the business inputs,
                        # not every owner that a later stage might select.
                        query=json.loads(command('implementation-authoring','run',json.dumps({
                            'argv':[sys.executable,'-B','.trellis/scripts/delivery.py','current','--json']})))
                        self.assertEqual(query['returncode'],0,query['stderr'])
                        self.assertEqual(json.loads(query['stdout'])['kind'],'current')
                        for name in ('SKILL.md','interface.json','commands.json'):
                            read(repository/'.trellis/guru-team/skills/packages/guru-clarify-requirements'/name)
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
                    invocation={'public_input':public,'owner_result':owner}
                    intermediate=command('guru-clarify-requirements','invoke',json.dumps(invocation),
                        ['--invocation','-'])
                    self.assertEqual(json.loads(intermediate),{'exit_id':'blocked'})
                    if initial_reads_complete:
                        with self.assertRaisesRegex(ValueError,
                                'implementation terminal stdout is not the final original wrapper result'):
                            implementation_authoring.validate_trace(
                                json.loads(Path(protocol['trace_path']).read_text()), protocol, intermediate)
                    stdout=command('guru-clarify-requirements','invoke',json.dumps({'final':True,
                        'invocation':invocation}),['--invocation','-'])
                    self.assertEqual(json.loads(stdout),{'exit_id':'blocked'})
                    if initial_reads_complete and not defer_owner_reads:
                        output_path=Path(protocol['model_root'])/'output/native-last-message.txt'
                        # Reproduce an ordinary model-output error. The original
                        # parser must reject it rather than trim the extra brace.
                        output_path.write_text(stdout+'}')
                        with self.assertRaises(json.JSONDecodeError):
                            native_adapter.unwrap_native_output('codex', stdout, output_path)
                        output_path.write_text(json.dumps(json.loads(stdout),ensure_ascii=False,indent=2))
                        stdout=native_adapter.unwrap_native_output('codex', '', output_path)
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
        import pty
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            fixture, source = stage_clean_installed_owner_repo(root / 'execution',
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            package = fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name
            self.stage_historical_fixture({'case_id':'native-implementation-plan-premise'}, fixture, package, source)
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
            preimages = {str(fixture / path):hashlib.sha256((fixture / path).read_bytes()).hexdigest()
                         for path in facts['writable_paths'] if (fixture / path).is_file()}
            def call(skill, command, arguments=(), *, stdin=None):
                command_argv = [*argv, '--skill-id', skill, '--command=' + command]
                if stdin is not None:
                    command_argv.append('--stdin')
                return subprocess.run([*command_argv, '--', *arguments],
                    input=stdin or '', capture_output=True, text=True, check=False, timeout=20)
            try:
                for relative in (implementation_authoring.FACTS, *facts['required_reads']):
                    read = subprocess.run([*argv[:-1], 'read', '--kind', 'owner_file',
                        '--path', str(fixture / relative)], capture_output=True, text=True, timeout=20)
                    self.assertEqual(read.returncode, 0, read.stderr)
                # An ordinary CLI query has no stdin or final marker. Stopping
                # here must identify the missing terminal wrapper precisely.
                current = call('delivery-api', 'current', ['--json'])
                self.assertEqual(current.returncode, 0, current.stderr)
                self.assertEqual(json.loads(current.stdout)['kind'], 'current')
                self.assertFalse(relay.terminal)
                with self.assertRaisesRegex(ValueError,
                        'implementation terminal stdout is not the final original wrapper result'):
                    implementation_authoring.validate_trace(json.loads(trace.read_text()), {
                        'implementation_receipts_path': str(receipts),
                        'repository_projection_root': str(fixture),
                        'writable_preimages': preimages}, current.stdout)
                master, slave = pty.openpty()
                try:
                    before_missing_stdin = len(relay.receipts)
                    missing_stdin = subprocess.run([*argv, '--skill-id', 'implementation-authoring',
                        '--command', 'run', '--stdin'], stdin=slave, capture_output=True,
                        text=True, check=False, timeout=5)
                    self.assertEqual(missing_stdin.returncode, 2)
                    self.assertIn('no request was sent', missing_stdin.stderr)
                    self.assertEqual(len(relay.receipts), before_missing_stdin)
                    self.assertFalse(relay.terminal)
                    top_help = subprocess.run([*argv, '--skill-id', 'delivery-api',
                        '--command=--help'], stdin=slave, capture_output=True,
                        text=True, check=False, timeout=20)
                    self.assertEqual(top_help.returncode, 0, top_help.stderr)
                finally:
                    os.close(master)
                    os.close(slave)
                final_marker = json.dumps({'final':True,'invocation':{}})
                count = len(relay.receipts)
                marked = call('delivery-api', '--help', stdin=final_marker)
                self.assertEqual(marked.returncode, 2)
                self.assertEqual(marked.stdout, '')
                self.assertIn('only an original semantic public wrapper', marked.stderr)
                self.assertEqual(len(relay.receipts), count + 1)
                self.assertFalse(relay.terminal)
                corrected_help = call('delivery-api', '--help')
                self.assertEqual(corrected_help.returncode, 0, corrected_help.stderr)
                self.assertIn('usage: delivery.py', corrected_help.stdout)
                count = len(relay.receipts)
                marked_recorder = call('guru-check-task', 'record-phase2-check', stdin=final_marker)
                self.assertEqual(marked_recorder.returncode, 2)
                self.assertIn('only an original semantic public wrapper', marked_recorder.stderr)
                self.assertEqual(len(relay.receipts), count + 1)
                marked_help = call(PACKAGE.name, 'invoke', ['--help'], stdin=final_marker)
                self.assertEqual(marked_help.returncode, 0, marked_help.stderr)
                self.assertIn('usage:', marked_help.stdout)
                self.assertFalse(relay.terminal)
                bad_index = len(relay.receipts)
                bad = call('delivery-api', 'apply', ['apply', '--input', '{}'])
                self.assertEqual(bad.returncode, 2)
                self.assertIn('unrecognized arguments: apply', bad.stderr)
                self.assertFalse(relay.terminal)
                self.assertTrue(thread.is_alive())
                missing = call('delivery-api', 'apply')
                self.assertEqual(missing.returncode, 2)
                self.assertIn('delivery.py apply: error:', missing.stderr)
                self.assertFalse(relay.terminal)
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
                self.assertFalse(relay.terminal)
                self.assertTrue(thread.is_alive())
                public = {'profile':'delivery_active_task_scope_change','mode':'workflow',
                    'task_ref':facts['task_ref'],'delivery_key':facts['delivery_key'],
                    'source_exit':'implementation_discovery','target_locator':'docs/implementation-observation.md',
                    'resume_target':'guru-resume-implementation','continuation_id':'transport-final-probe'}
                owner = {'public_input':public,'typed_exit':'blocked',
                    'reason':'Mechanical transport probe only; native judgment is separate.',
                    'ai_review_gate':{'status':'blocked','summary':'No native semantic result is asserted.'}}
                terminal = call('guru-clarify-requirements', 'invoke', ['--invocation','-'],
                    stdin=json.dumps({'final':True,'invocation':{'public_input':public,'owner_result':owner}}))
                self.assertEqual(terminal.returncode, 0, terminal.stderr)
                self.assertEqual(json.loads(terminal.stdout), {'exit_id':'blocked'})
                self.assertTrue(relay.terminal)
                rows = json.loads(receipts.read_text())
                self.assertEqual(rows[bad_index]['request']['arguments'], ['apply', '--input', '{}'])
                self.assertEqual(rows[bad_index]['response']['stderr'], bad.stderr)
                payload = json.loads(trace.read_text())
                payload['terminal_skill_id'] = 'guru-clarify-requirements'
                self.assertEqual(len([event for event in payload['events'] if event['kind']=='command']), len(rows))
                implementation_authoring.validate_trace(payload, {
                    'implementation_receipts_path':str(receipts),'repository_projection_root':str(fixture),
                    'writable_preimages':preimages}, terminal.stdout)
                receipt_count = len(relay.receipts)
                after_terminal = call('delivery-api', 'contract', ['--json'])
                self.assertEqual(after_terminal.returncode, 2)
                self.assertEqual(after_terminal.stdout, '')
                self.assertIn('follows the terminal original wrapper', after_terminal.stderr)
                self.assertTrue(relay.terminal)
                self.assertTrue(thread.is_alive())
                self.assertEqual(len(relay.receipts), receipt_count + 1)
                execution_relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ), root / 'execution-error.json')
                execution_error = execution_relay.forward({'skill_id':'delivery-api','command':'apply',
                    'arguments':['--task',facts['task_ref'],'--input','{}'],'stdin':''})
                self.assertEqual(execution_error['returncode'], 1)
                self.assertFalse(execution_relay.terminal)
            finally:
                stop.set()
                thread.join(timeout=2)

    def test_code_observation_records_actual_probe_without_a_design_verdict(self):
        with tempfile.TemporaryDirectory() as temporary:
            execution = Path(temporary) / 'execution'
            fixture, source = stage_clean_installed_owner_repo(
                execution, REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            package = fixture / '.trellis/guru-team/skills/packages/guru-check-task'
            self.stage_historical_fixture({'case_id':'native-implementation-code-drift'}, fixture, package, source)
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
            self.assertNotEqual(after['reviewed_content']['sha256'],first['reviewed_content']['sha256'])
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
            self.stage_historical_fixture({'case_id': 'native-implementation-plan-premise'}, fixture, package, source)
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
            author_arguments=['--input',json.dumps(author_public),'--owner-result','-']
            invalid=relay.forward({'skill_id':'guru-author-task-plan','command':'invoke',
                'arguments':author_arguments,'stdin':''})
            self.assertNotEqual(invalid['returncode'],0)
            self.assertEqual(json.loads(invalid['stdout'])['code'],'invalid_json')
            self.assertFalse(relay.terminal)
            authored=relay.forward({'skill_id':'guru-author-task-plan','command':'invoke',
                'arguments':author_arguments,'stdin':json.dumps({
                    'public_input':author_public,'output':author_output,'ai_review_gate':{
                        'status':'passed','summary':'Objective C5 and original wrapper transport only.'}})})
            self.assertEqual(authored['returncode'],0,authored['stderr'])
            self.assertEqual(json.loads(authored['stdout']),author_output)
            from adapters.eval import stage_result_authoring
            stage_relay=stage_result_authoring.ImplementationCommands(fixture,dict(os.environ),
                fixture.parent/'author-consumption-receipts.json',
                facts_relative=implementation_authoring.FACTS)
            transient=fixture/'.trellis/.runtime/guru-team/evals/author-owner.json'
            transient.parent.mkdir(parents=True,exist_ok=True)
            transient.write_text(json.dumps({'public_input':author_public,'output':author_output,
                'ai_review_gate':{'status':'passed','summary':'Objective file consumption transport only.'}}))
            facts_before = (fixture / implementation_authoring.FACTS).read_bytes()
            consumed=stage_relay.forward({'skill_id':'guru-author-task-plan','command':'invoke',
                'arguments':['--input',json.dumps(author_public),'--owner-result',str(transient)],'stdin':''})
            self.assertEqual(consumed['returncode'],0,consumed['stderr'])
            self.assertEqual(json.loads(consumed['stdout']),author_output)
            self.assertFalse(transient.exists())
            self.assertIn(transient.relative_to(fixture).as_posix(), stage_relay.consumed_paths)
            self.assertEqual((fixture / implementation_authoring.FACTS).read_bytes(), facts_before)
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
        worker.write_text(f'#!{sys.executable}\n' + textwrap.dedent('''\
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
            print('native diagnostic transport only', file=sys.stderr)
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
        worker.chmod(0o755)
        callback=native_adapter.implementation_reviewer(protocol,commands,
            [str(worker),'exec','--output-last-message',str(root/'unused'),'overall'],dict(os.environ),
            persisted_observation=True)
        shutil.rmtree(repository/'.trellis/tasks/implementation-evidence')
        with self.assertRaisesRegex(ValueError, 'ordered reads'):
            callback({'public_input':public})
        self.assertFalse((model/'architecture-worker-01').exists())
        authorities = ['docs/architecture/00-foundation/design-constitution.md',
            'docs/architecture/README.md', 'docs/architecture/06-governance/change-contract.md']
        with self.assertRaisesRegex(ValueError, 'in that order'):
            callback({'public_input':public,'reads':[authorities[1],authorities[0],authorities[2]]})
        with self.assertRaisesRegex(ValueError, 'exclude Task PRD'):
            callback({'public_input':public,'reads':[*authorities,facts['task_ref']+'/prd.md']})
        self.assertFalse((model/'architecture-worker-01').exists())
        result=callback({'public_input':public,'reads':[
            'docs/architecture/00-foundation/design-constitution.md','docs/architecture/README.md',
            'docs/architecture/06-governance/change-contract.md',facts['planning_root']+'/design.md',
            'interval.py','range_filter.py','docs/range.md']})
        self.assertEqual(result['returncode'],0,result['stderr'])
        self.assertEqual(json.loads(result['stdout'])['exit_id'],'baseline_current')
        self.assertEqual(result['stderr'], '')
        execution=json.loads((private/'implementation-architecture-executions.json').read_text())[0]
        self.assertFalse(execution['fresh_ephemeral'])
        self.assertIn('This fresh independent worker', execution['context'])
        self.assertNotIn('fresh ephemeral', execution['context'])
        observation = Path(execution['wrapper_observation_path'])
        self.assertEqual(observation.parent, private)
        captured = json.loads(observation.read_text())
        self.assertEqual(captured['wrapper']['stdout'], execution['stdout'])
        self.assertEqual(native_adapter.unwrap_native_output('codex',
            captured['wrapper']['stdout'], None), result['stdout'])
        self.assertEqual(captured['wrapper']['returncode'], 0)
        self.assertEqual(json.loads(captured['stdin'])['public_input'], public)
        self.assertIn('native diagnostic transport only', execution['stderr'])
        trace=json.loads(Path(execution['trace_path']).read_text())
        self.assertEqual(sum(event['kind']=='invoke' for event in trace['events']),1)
        self.assertEqual((model/'native-context.txt').read_text(),'Overall implementation context.')
        # A normal schema mistake must retain the original wrapper diagnostic
        # for the next invocation, without turning the failure into a result.
        invalid = dict(public, schema_version='3.0')
        failed=callback({'public_input':invalid,'reads':[
            'docs/architecture/00-foundation/design-constitution.md','docs/architecture/README.md',
            'docs/architecture/06-governance/change-contract.md',facts['planning_root']+'/design.md',
            'interval.py','range_filter.py','docs/range.md']})
        self.assertEqual(failed['returncode'],2)
        self.assertEqual(failed['stdout'],'')
        self.assertIn('original Architecture wrapper failed:',failed['stderr'])
        self.assertIn('schema_mismatch',failed['stderr'])
        execution=json.loads((private/'implementation-architecture-executions.json').read_text())[-1]
        self.assertIn(execution['stdout'].strip(),failed['stderr'])
        captured = json.loads(Path(execution['wrapper_observation_path']).read_text())
        self.assertNotEqual(captured['wrapper']['returncode'], 0)
        self.assertIn('schema_mismatch', captured['wrapper']['stdout'])

    def test_contract_overlap_keeps_original_architecture_conflict_at_callback(self):
        # Supply only the native-process boundary in this module test. This
        # exercises the real callback/validator, not native judgment or a wrapper.
        from adapters.eval.eval_constants import stdout_digest
        from types import SimpleNamespace
        source = SKILLS / 'packages/guru-maintain-architecture-baseline'
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            model = root / 'model'; model.mkdir()
            repository = model / 'repository'; repository.mkdir()
            private = root / 'private-control'; private.mkdir()
            package = repository / '.trellis/guru-team/skills/packages' / source.name
            shutil.copytree(source, package)
            (model / 'native-context.txt').write_text('Original parent context.')
            public = json.loads((package / 'examples/public-input-delivery-task-impact-sync-1.0.json').read_text())
            public['stage'] = 'planning'
            authorities = [public['constitution']['authority_locator'], public['baseline']['locator'],
                public['project_contract']['change_contract_locator']]
            overlaps = [str((package / name).relative_to(repository)) for name in (
                'SKILL.md', 'interface.json', 'references/contract.md',
                'schemas/public-input-delivery-task-impact-sync-3.0.schema.json')]
            reads = [*authorities, *overlaps, 'changed-contract.patch', 'unchanged_caller.py']
            raw = json.dumps({'exit_id': 'architecture_conflict', 'return_route': 'planning'},
                separators=(',', ':')) + '\n'
            early_candidate = False

            def native_process(argv, output_path, context, **kwargs):
                paths = architecture_authoring.public_contract_reads(package, public)
                paths += [repository / path for path in authorities]
                paths += [repository / 'changed-contract.patch', repository / 'unchanged_caller.py']
                paths.append(repository / '.trellis/tasks/implementation-evidence' /
                    ('architecture-facts-' + output_path.parent.name.rsplit('-', 1)[1] + '.json'))
                events = [{'kind': 'read', 'path': str(path)} for path in paths]
                if early_candidate:
                    events.insert(1, {'kind': 'read', 'path': str(repository / 'changed-contract.patch')})
                events.append({'kind': 'invoke', 'returncode': 0, 'stdout_sha256': stdout_digest(raw)})
                (output_path.parent / 'native-trace.json').write_text(json.dumps({'events': events}))
                output_path.write_text(raw)
                return subprocess.CompletedProcess(argv, 0, raw, '')

            protocol = {'repository_projection_root': str(repository), 'model_root': str(model),
                'owner_repository': str(root / 'owner'), 'private_root': str(private),
                'request_sha256': 'a' * 64}
            # The host boundary checks the real owner wrapper's availability.
            owner_package = Path(protocol['owner_repository']) / '.trellis/guru-team/skills/packages' / source.name
            # The real callback reads current public assets from the owner.
            shutil.copytree(source, owner_package)
            owner_wrapper = owner_package / 'scripts/invoke.sh'
            owner_wrapper.write_bytes((source / 'scripts/invoke.sh').read_bytes())
            owner_wrapper.chmod(0o755)
            callback = native_adapter.implementation_reviewer(protocol, SimpleNamespace(environment={}),
                ['codex', 'exec', '--ephemeral', '--output-last-message', str(root / 'unused'), 'parent'], {})
            with patch.object(architecture_authoring, 'execute_reviewer', side_effect=native_process):
                response = callback({'public_input': public, 'reads': reads})
                self.assertEqual(response, {'returncode': 0,
                    'stdout': native_adapter.unwrap_native_output('codex', raw, None), 'stderr': ''})
                self.assertEqual(json.loads(response['stdout'])['exit_id'], 'architecture_conflict')
                early_candidate = True
                rejected = callback({'public_input': public, 'reads': reads})
                self.assertEqual(rejected['returncode'], 2)
                self.assertIn('authority before candidate', rejected['stderr'])
            self.assertEqual((model / 'native-context.txt').read_text(), 'Original parent context.')

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
            self.stage_historical_fixture({'case_id':'native-implementation-plan-premise'},fixture,
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
            self.stage_historical_fixture({'case_id':'native-implementation-plan-premise'},fixture,
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
            self.stage_historical_fixture({'case_id':'native-implementation-plan-premise'},fixture,
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
        for approval_command in ('invoke', 'invoke-guru-approve-task-plan'):
            with self.subTest(approval_command=approval_command), tempfile.TemporaryDirectory() as temporary:
                root=Path(temporary)
                fixture,source=stage_clean_installed_owner_repo(root/'execution',
                    REPO/'.trellis/guru-team/scripts/bash/run-skill-command.sh',PACKAGE)
                self.stage_historical_fixture({'case_id':'native-implementation-plan-premise'},fixture,
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
                    'request':{'skill_id':'guru-approve-task-plan','command':approval_command},
                    'response':{'returncode':0,'stdout':json.dumps(approved)}}]))
                protocol=root/'first-protocol.json';protocol.write_text(json.dumps({
                    'native_request_path':str(first_request),'owner_repository':str(fixture),
                    'implementation_receipts_path':str(receipts)}))
                output=root/'activation-output.json';output.write_text(json.dumps(activation))
                request={'skill_id':PACKAGE.name,'case_id':implementation_authoring.RESUME_CASE,
                         'package_root':str(PACKAGE)}
                with patch.dict(os.environ,{implementation_authoring.RESUME_PROTOCOL_ENV:str(protocol),
                                            implementation_authoring.ACTIVATION_OUTPUT_ENV:str(output)}):
                    original_receipts=receipts.read_bytes()
                    for wrong_command in ('record-planning-approval', 'invoke-guru-check-task'):
                        wrong_receipts=json.loads(original_receipts)
                        wrong_receipts[-1]['request']['command']=wrong_command
                        receipts.write_text(json.dumps(wrong_receipts))
                        with self.assertRaisesRegex(ValueError,'actual original Approval stdout'):
                            implementation_authoring.resume_execution(request)
                        self.assertFalse((fixture/implementation_authoring.RESUME_FACTS).exists())
                    receipts.write_bytes(original_receipts)
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

class R1RequestEntryTests(unittest.TestCase):
    """Module evidence only; no native judgment or Intake readiness is supplied."""

    def entry(self, root):
        from adapters.eval.test_native_constraint_transport import request as native_request
        request = native_request(root, PACKAGE.name, 'native-implementation-plan-premise')
        fixture, source = stage_clean_installed_owner_repo(root / 'execution',
            REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
        fixture = fixture.resolve()
        with patch.object(phase2_authoring, 'stage', side_effect=AssertionError('no Task seed')):
            implementation_authoring.stage(request, fixture,
                fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name, source)
        environment = {**os.environ, **implementation_authoring.entry_environment(fixture)}
        return request, fixture, environment

    def test_public_json_errors_match_original_wrapper_through_same_fifo(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            _, fixture, environment = self.entry(root)
            package = fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name
            discovery = fixture / '.trellis/guru-team/skills/packages/guru-discover-change-context'
            relay = implementation_authoring.ImplementationCommands(fixture, environment, root / 'receipts.json')
            stop = threading.Event()
            request_fifo, response_fifo = root / 'request', root / 'response'
            thread = native_adapter.start_qualification_runtime_boundary(request_fifo, response_fifo,
                stop, fixture, package, environment, {}, implementation_commands=relay)
            helper = root / 'helper.py'
            helper.write_text(qualification_trace_helper_source(allow_commands=True))
            argv = [sys.executable, '-B', str(helper), '--trace', str(root / 'trace.json'),
                '--request-sha256', '1' * 64, '--projection-root', str(package),
                '--repository-root', str(fixture), '--sandbox-root', str(root),
                '--request-fifo', str(request_fifo), '--response-fifo', str(response_fifo),
                '--skill-sha256', '2' * 64, '--wrapper-sha256', '3' * 64,
                'command', '--skill-id', 'guru-discover-change-context']

            def forwarded(command, arguments, body):
                return subprocess.run([*argv, '--command', command, '--stdin', '--', *arguments],
                    input=body, capture_output=True, text=True, check=False, timeout=20)

            try:
                arguments = ['--root', '.', '--invocation', '-']
                for body in ('\n', '{'):
                    with self.subTest(body=body):
                        direct = subprocess.run([str(discovery / 'scripts/check-context-discovery.sh'),
                            *arguments], input=body, cwd=fixture, env=environment,
                            capture_output=True, text=True, check=False, timeout=20)
                        self.assertEqual(direct.returncode, 2)
                        error = json.loads(direct.stdout)
                        self.assertEqual((error['code'], error['field_path']), ('invalid_json', 'invocation'))
                        actual = forwarded('check-context-discovery', arguments, body)
                        self.assertEqual((actual.returncode, actual.stdout, actual.stderr),
                                         (direct.returncode, direct.stdout, direct.stderr))
                        self.assertEqual(relay.receipts[-1]['request']['stdin'], body)
                        self.assertEqual(relay.receipts[-1]['response'], {
                            'returncode': direct.returncode, 'stdout': direct.stdout, 'stderr': direct.stderr})
                        self.assertFalse(relay.terminal)
                        self.assertTrue(thread.is_alive())
                # The original fact query still runs through the same service
                # after both errors; no semantic owner result is supplied.
                valid = forwarded('preview-change-context-history',
                    ['--root', '.', '--query-json', json.dumps({'paths': ['interval.py']})], '')
                self.assertEqual(valid.returncode, 0, valid.stderr)
                self.assertFalse(json.loads(valid.stdout)['formal_exit'])
                self.assertFalse(relay.terminal)
            finally:
                stop.set()
                thread.join(timeout=2)

    def planning_child_fixture(self, root):
        # Creation and accepted scope are module preconditions, not native
        # Intake or semantic approval evidence. Project before any Task exists.
        from runtime.delivery_projection.adapter import authority_ref
        _, fixture, environment = self.entry(root)
        model = root / 'child-model'; model.mkdir()
        repository = model / 'repository'
        stage_repository_projection(fixture, repository)
        self.assertFalse(list((repository / '.trellis/tasks').glob('*/task.json')))
        (model / 'native-context.txt').write_text('Parent transport context.')
        private = root / 'private-control'; private.mkdir()
        relay = implementation_authoring.ImplementationCommands(fixture, environment,
            private / 'creation-receipts.json')
        task_id = 'r1-planning-entry'
        task_ref = '.trellis/tasks/' + datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%m-%d-') + task_id
        head = run_git(fixture, 'rev-parse', 'HEAD')
        public = {'profile': 'delivery_task_creation', 'action': 'create_task',
            'creation': {'task_id': task_id, 'task_ref': task_ref,
                'source_profile': 'standalone_request', 'reviewed_source': {'kind': 'no_issue'},
                'accepted_scope_identity': 'scope:module-r1',
                'delivery_target': {'repo_ref': 'example/guru-extension', 'branch_ref': 'main'},
                'selected_base_ref': 'main', 'reviewed_base_source': {'kind': 'synced_branch', 'selected_ref': 'main', 'commit': head}},
            'acquisition': {'route': 'adopt_invocation_checkout',
                'branch_ref': 'refs/heads/codex/eval-r1-planning-entry', 'decision_head': head,
                'transaction_id': 'module-child-acquisition', 'result_id': 'module-child-checkout',
                'invocation_checkout': str(fixture)},
            'task': {'title': 'R1 child transport', 'description': 'Module file visibility only.',
                     'scope': 'R1 integer range'}}
        created = relay.forward({'skill_id': 'guru-create-task', 'command': 'invoke',
            'arguments': ['--input', json.dumps(public)], 'stdin': ''})
        self.assertEqual(created['returncode'], 0, created['stdout'] or created['stderr'])
        self.assertEqual(json.loads(created['stdout'])['exit_id'], 'created')
        relay.forward({'skill_id': 'implementation-authoring', 'command': 'observe-entry',
            'arguments': [], 'stdin': json.dumps({'producer_skill': 'guru-create-task',
                                                 'producer_stdout': created['stdout']})})
        task = fixture / task_ref
        task.joinpath('prd.md').write_bytes((fixture / 'docs/requests/r1.md').read_bytes())
        projection = DeliveryProjection(fixture, task_ref)
        scope = authority_ref(task / 'prd.md', fixture)
        projection.scope(scope)
        public = {'profile': 'delivery_creation', 'mode': 'workflow', 'task_ref': task_ref,
            'task_key': {'task_id': task_id, 'lifecycle_generation': 0},
            'scope_ref': {'authority': scope, 'anchors': ['R1']},
            'delivery_profile': 'pull_request', 'continuation_id': 'module-child-delivery', 'action': 'create'}
        created = relay.forward({'skill_id': 'guru-create-delivery', 'command': 'invoke',
            'arguments': ['--input', json.dumps(public), '--owner-result', json.dumps({
                'typed_exit': 'created', 'reason': 'Module transport precondition only.'})], 'stdin': ''})
        self.assertEqual(created['returncode'], 0, created['stdout'] or created['stderr'])
        self.assertEqual(json.loads(created['stdout'])['exit_id'], 'created', created['stdout'])
        relay.forward({'skill_id': 'implementation-authoring', 'command': 'observe-entry',
            'arguments': [], 'stdin': json.dumps({'producer_skill': 'guru-create-delivery',
                                                 'producer_stdout': created['stdout']})})
        staged = relay.forward({'skill_id': 'implementation-authoring', 'command': 'stage-candidate',
                                'arguments': [], 'stdin': '{}'})
        self.assertEqual(staged['returncode'], 0, staged['stderr'])
        facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
        self.assertFalse((repository / facts['planning_root'] / 'design.md').exists())
        self.assertFalse((repository / 'docs/phase2-evidence/diff.patch').exists())
        protocol = {'repository_projection_root': str(repository), 'model_root': str(model),
            'owner_repository': str(fixture), 'private_root': str(private), 'request_sha256': 'a' * 64}
        return fixture, repository, relay, facts, protocol

    def read_planning_child(self, fixture, repository, relay, facts, protocol, purpose):
        # Only inference is replaced. A separate Python process executes every
        # actual child helper read; it supplies no typed exit or semantic gate.
        package = fixture / '.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline'
        public = json.loads((package / 'examples/public-input-candidate-assessment-3.0.json').read_text())
        design = facts['planning_root'] + '/design.md'
        public.update(schema_version='delivery-1.0', profile='delivery_task_impact_sync',
            task_locator=facts['task_ref'], delivery_key=facts['delivery_key'],
            planning_root=Path(facts['planning_root']).relative_to(facts['task_ref']).as_posix(),
            planning_purpose=purpose, requirement_authority='docs/range.md', behavior_authority='docs/range.md',
            freshness_identity='sha256:' + hashlib.sha256((fixture / design).read_bytes()).hexdigest())
        public['baseline']['identity'] = 'range-v1'
        public['constitution']['identity'] = 'range-constitution-v1'
        public['project_contract'].update(change_contract_identity='range-contract-v1',
                                         required_concern_set_identity='range-concerns-v1')
        if purpose == 'candidate_assessment':
            public['candidate'] = {'design_locator': design}
        else:
            public.pop('candidate')
            public['design_locator'] = design
        authorities = [public['constitution']['authority_locator'], public['baseline']['locator'],
                       public['project_contract']['change_contract_locator']]
        reads = [*authorities, design, 'docs/phase2-evidence/diff.patch',
                 'interval.py', 'range_filter.py', 'test_interval.py', 'docs/range.md']
        observations = []
        traces = []

        def child_process(argv, output_path, context, **kwargs):
            probe = textwrap.dedent('''\
                import json,shlex,subprocess,sys
                commands=[shlex.split(line) for line in sys.stdin.read().splitlines()
                          if line.startswith('/') and ' read --kind ' in line]
                contents={}
                for command in commands:
                    result=subprocess.run(command,capture_output=True,check=False)
                    if result.returncode:
                        sys.stderr.buffer.write(result.stderr)
                        raise SystemExit(result.returncode)
                    contents[command[command.index('--path')+1]]=result.stdout.hex()
                print(json.dumps({'contents':contents}))
                ''')
            actual = subprocess.run([sys.executable, '-B', '-c', probe], input=context,
                cwd=kwargs['cwd'], env=kwargs['environment'], capture_output=True, text=True, check=False)
            self.assertEqual(actual.returncode, 0, actual.stderr or actual.stdout)
            observations.append(json.loads(actual.stdout)['contents'])
            events = json.loads((output_path.parent / 'native-trace.json').read_text())['events']
            index = output_path.parent.name.rsplit('-', 1)[1]
            architecture_authoring.validate_reviewer_reads(events, repository,
                [*reads, '.trellis/tasks/implementation-evidence/architecture-facts-' + index + '.json'],
                phase2=False, contract_reads=architecture_authoring.public_contract_reads(
                    repository / '.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline', public))
            traces.append(events)
            output_path.write_text(actual.stdout)
            return subprocess.CompletedProcess(argv, actual.returncode, actual.stdout,
                'Module read probe only; no native semantic invocation was executed.')

        if not hasattr(relay, 'projection_callback'):
            relay.projection_callback = native_adapter.implementation_reviewer(protocol, relay,
                [sys.executable, 'exec', '--ephemeral', '--output-last-message', 'unused', 'parent'], relay.environment)
        before = repository_file_inventory(fixture)
        with patch.object(architecture_authoring, 'execute_reviewer', side_effect=child_process):
            response = relay.projection_callback({'public_input': public, 'reads': reads})
        # The probe ends at reads. The real callback must retain its incomplete
        # invocation diagnostic rather than turn these reads into Architecture pass.
        self.assertEqual(response['returncode'], 2)
        self.assertEqual(response['stdout'], '')
        self.assertIn('did not return its actual original wrapper stdout', response['stderr'])
        self.assertEqual(repository_file_inventory(fixture), before)
        self.assertEqual(len(observations), 1)
        for relative in reads:
            expected = (fixture / relative).read_bytes()
            self.assertEqual(bytes.fromhex(observations[0][str(repository / relative)]), expected)
            self.assertEqual((repository / relative).read_bytes(), expected)
        self.assertFalse((repository / '.git').exists())
        self.assertFalse((repository / '.trellis/.runtime').exists())
        self.assertFalse((repository / '.trellis/guru-team/runtime').exists())
        self.assertFalse(any(Path(event['path']).name in {'prd.md', 'implement.md', 'task.json'}
                             for event in traces[0]))
        return observations[0]

    def test_architecture_child_reads_new_planning_files_after_creation(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture, repository, relay, facts, protocol = self.planning_child_fixture(Path(temporary).resolve())
            self.read_planning_child(fixture, repository, relay, facts, protocol, 'candidate_assessment')

    def test_architecture_child_refreshes_rewritten_design_and_diff(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture, repository, relay, facts, protocol = self.planning_child_fixture(Path(temporary).resolve())
            first = self.read_planning_child(fixture, repository, relay, facts, protocol, 'candidate_assessment')
            for relative in [facts['planning_root'] + '/design.md', 'docs/phase2-evidence/diff.patch']:
                (fixture / relative).write_bytes((fixture / relative).read_bytes() + b'\nSecond authoring round.\n')
            # A new child keeps its own first-read trace and authority order.
            second = self.read_planning_child(fixture, repository, relay, facts, protocol, 'final_plan')
            for relative in [facts['planning_root'] + '/design.md', 'docs/phase2-evidence/diff.patch']:
                self.assertNotEqual(first[str(repository / relative)], second[str(repository / relative)])

    def test_request_entry_exposes_original_brainstorm_method(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, fixture, _ = self.entry(root)
            relative = Path('.agents/skills/trellis-brainstorm/SKILL.md')
            source = REPO / relative
            expected_bytes = source.read_bytes()
            expected_mode = source.stat().st_mode & 0o777
            primary = fixture.with_name('owner-repo-primary')
            projected = root / 'public-repository'
            stage_repository_projection(fixture, projected)
            for repository in (fixture, primary, projected):
                self.assertEqual((repository / relative).read_bytes(), expected_bytes)
                self.assertEqual((repository / relative).stat().st_mode & 0o777, expected_mode)
            committed = subprocess.check_output(['git', 'show', 'HEAD:' + relative.as_posix()], cwd=fixture)
            self.assertEqual(committed, expected_bytes)
            for private in ('.git', '.trellis/.runtime', '.trellis/guru-team/runtime',
                            '.trellis/guru-team/skills/adapters'):
                self.assertFalse((projected / private).exists())

    def test_missing_request_method_stops_before_native(self):
        from adapters.eval.test_native_constraint_transport import request as native_request
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = native_request(root, PACKAGE.name, 'native-implementation-plan-premise')
            fixture = root / 'empty-fixture'
            fixture.mkdir()
            source = root / 'incomplete-source'
            source.mkdir()
            with patch.object(implementation_authoring, 'run_git') as git, \
                    patch.object(implementation_authoring, 'stage_planning_snapshot') as snapshot:
                with self.assertRaisesRegex(ValueError, 'original trellis-brainstorm method.*matching installed source'):
                    implementation_authoring.stage(request, fixture, PACKAGE, source)
            git.assert_not_called()
            snapshot.assert_not_called()
            self.assertEqual(list(fixture.iterdir()), [])

    def test_request_seed_is_clean_and_has_no_business_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            request, fixture, environment = self.entry(Path(temporary))
            primary = fixture.with_name('owner-repo-primary')
            self.assertEqual(run_git(fixture, 'status', '--porcelain'), '')
            self.assertEqual(run_git(primary, 'status', '--porcelain'), '')
            self.assertEqual(run_git(fixture, 'rev-parse', 'HEAD'), run_git(primary, 'rev-parse', 'HEAD'))
            self.assertFalse(list((fixture / '.trellis/tasks').glob('*/task.json')))
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            self.assertTrue(all((fixture / path).is_file() for path in facts['required_reads']))
            self.assertIn(implementation_authoring.FACTS, facts['writable_paths'])
            for key in ('task_ref', 'delivery_key', 'source_selection', 'current_delivery'):
                self.assertNotIn(key, facts)
            self.assertIn('raise NotImplementedError', (fixture / 'interval.py').read_text())
            self.assertIn('self.assertFalse(contains(4, 2, 4))', (fixture / 'test_interval.py').read_text())
            observed = subprocess.run([sys.executable, '-B', '.trellis/scripts/task.py', 'current', '--json'],
                cwd=fixture, env=environment, capture_output=True, text=True, check=False)
            # The original current command returns 1 for a healthy no-Task state.
            self.assertEqual(observed.returncode, 1, observed.stdout or observed.stderr)
            current = json.loads(observed.stdout)
            self.assertIsNone(current['current_task'])
            self.assertFalse(current['stale'])
            self.assertNotIn('error', current)
            # A real local remote is fetched; the transport cannot synthesize Sync success.
            fetch = subprocess.run(['git', 'fetch', 'origin', 'main'], cwd=primary,
                env=environment, capture_output=True, text=True, check=False)
            self.assertEqual(fetch.returncode, 0, fetch.stderr)
            self.assertEqual(run_git(primary, 'rev-parse', 'origin/main'), run_git(primary, 'rev-parse', 'HEAD'))

    def test_missing_request_entry_does_not_fall_back_to_a_task_snapshot(self):
        from adapters.eval.test_native_constraint_transport import request as native_request
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = native_request(root, PACKAGE.name, 'native-implementation-plan-premise')
            path = Path(request['workdir']) / request['files'][0]
            body = json.loads(path.read_text()); body.pop('entry_kind')
            path.write_text(json.dumps(body))
            with patch.object(implementation_authoring, 'stage_planning_snapshot') as snapshot:
                with self.assertRaisesRegex(ValueError, 'declared pre_task_r1 source request'):
                    implementation_authoring.stage(request, root / 'not-created', PACKAGE, REPO)
            snapshot.assert_not_called()
            self.assertFalse((root / 'not-created').exists())

    def test_observation_consumes_actual_task_creator_stdout_and_tracks_fact_versions(self):
        # The reviewed creation input is a module precondition. This does not
        # claim that a native Agent performed the earlier Intake reviews.
        with tempfile.TemporaryDirectory() as temporary:
            _, fixture, environment = self.entry(Path(temporary))
            relay = implementation_authoring.ImplementationCommands(fixture, environment,
                fixture.parent / 'creation-receipts.json')
            before = (fixture / implementation_authoring.FACTS).read_bytes()
            with self.assertRaisesRegex(ValueError, 'complete actual creator stdout'):
                relay.observe_entry({'producer_skill': 'guru-create-task', 'producer_stdout': ''})
            self.assertEqual((fixture / implementation_authoring.FACTS).read_bytes(), before)
            task_id = 'r1-planning-entry'
            task_ref = '.trellis/tasks/' + datetime.now(ZoneInfo('Asia/Shanghai')).strftime('%m-%d-') + task_id
            head = run_git(fixture, 'rev-parse', 'HEAD')
            public = {'profile': 'delivery_task_creation', 'action': 'create_task',
                'creation': {'task_id': task_id, 'task_ref': task_ref,
                    'source_profile': 'standalone_request', 'reviewed_source': {'kind': 'no_issue'},
                    'accepted_scope_identity': 'scope:module-r1',
                    'delivery_target': {'repo_ref': 'example/guru-extension', 'branch_ref': 'main'},
                    'selected_base_ref': 'main', 'reviewed_base_source': {'kind': 'synced_branch', 'selected_ref': 'main', 'commit': head}},
                'acquisition': {'route': 'adopt_invocation_checkout',
                    'branch_ref': 'refs/heads/codex/eval-r1-planning-entry', 'decision_head': head,
                    'transaction_id': 'module-r1-acquisition', 'result_id': 'module-r1-checkout',
                    'invocation_checkout': str(fixture)},
                'task': {'title': 'R1 module transport', 'description': 'Original creator transport only.',
                         'scope': 'R1 integer range'}}
            created = relay.forward({'skill_id': 'guru-create-task', 'command': 'invoke',
                'arguments': ['--input', json.dumps(public)], 'stdin': ''})
            self.assertEqual(created['returncode'], 0, created['stderr'] or created['stdout'])
            self.assertEqual(json.loads(created['stdout'])['exit_id'], 'created')
            self.assertEqual(relay.receipts[-1]['target_states_after'][implementation_authoring.FACTS],
                             hashlib.sha256(before).hexdigest())
            output = relay.forward({'skill_id': 'implementation-authoring', 'command': 'observe-entry',
                'arguments': [], 'stdin': json.dumps({'producer_skill': 'guru-create-task',
                                                     'producer_stdout': created['stdout']})})
            self.assertEqual(output['returncode'], 0, output['stderr'])
            facts = json.loads((fixture / implementation_authoring.FACTS).read_text())
            self.assertEqual(facts['task_ref'], json.loads(created['stdout'])['task_ref'])
            self.assertEqual(facts['required_reads'], json.loads(before)['required_reads'])
            self.assertNotIn('source_selection', facts)
            self.assertNotIn('delivery_key', facts)
            task = json.loads((fixture / task_ref / 'task.json').read_text())
            self.assertIsNone(task['accepted_scope'])
            self.assertEqual(task['deliveries'], [])
            self.assertEqual(relay.receipts[-1]['target_states_after'][implementation_authoring.FACTS],
                             hashlib.sha256((fixture / implementation_authoring.FACTS).read_bytes()).hexdigest())

    def test_candidate_setup_preserves_scope_and_uses_observed_planning_directory(self):
        # Existing state is outside this byte-writer test's boundary. The
        # current projection double carries that actual installed record only.
        with tempfile.TemporaryDirectory() as temporary:
            fixture, source = stage_clean_installed_owner_repo(Path(temporary) / 'execution',
                REPO / '.trellis/guru-team/scripts/bash/run-skill-command.sh', PACKAGE)
            implementation_authoring.stage_planning_snapshot({'case_id': 'native-implementation-plan-premise'},
                fixture, fixture / '.trellis/guru-team/skills/packages' / PACKAGE.name, source)
            facts_path = fixture / implementation_authoring.FACTS
            facts = json.loads(facts_path.read_text())
            source_case = json.loads((PACKAGE / 'evals/files/native-implementation-plan-premise-input.json').read_text())
            facts.update(entry_kind=implementation_authoring.ENTRY_KIND,
                         candidate_seed=source_case['candidate_files'])
            facts['writable_paths'].append(implementation_authoring.FACTS)
            facts_path.write_text(json.dumps(facts))
            projection = DeliveryProjection(fixture, facts['task_ref'])
            current = {'kind': 'current', 'key': facts['delivery_key'],
                       'delivery': projection.resolve(facts['delivery_key'])}
            protected = {path: (fixture / path).read_bytes() for path in (
                facts['task_ref'] + '/task.json', facts['task_ref'] + '/prd.md', 'test_interval.py')}
            relay = implementation_authoring.ImplementationCommands(fixture, dict(os.environ),
                fixture.parent / 'seed-receipts.json')
            payload = {'skill_id': 'implementation-authoring', 'command': 'stage-candidate',
                       'arguments': [], 'stdin': '{}'}
            task = json.loads((fixture / facts['task_ref'] / 'task.json').read_text())
            def query(script, *arguments):
                return current if script == 'delivery.py' else {'current_task': {
                    'dir': facts['task_ref'], 'accepted_scope': task['accepted_scope']}}
            with patch.object(relay, 'public_query', side_effect=query):
                result = relay.forward(payload)
                self.assertEqual(result['returncode'], 0)
                self.assertEqual((fixture / 'interval.py').read_text(), source_case['candidate_files']['interval.py'])
                self.assertEqual(json.loads(result['stdout'])['validation']['returncode'], 0)
                with self.assertRaisesRegex(ValueError, 'already written'):
                    relay.forward(payload)
            for path, body in protected.items():
                self.assertEqual((fixture / path).read_bytes(), body)
            self.assertFalse(relay.terminal)
            self.assertNotIn('exit_id', json.loads(result['stdout']))

    def test_r1_carrier_profile_preserves_and_restores_existing_config(self):
        for ordinary_error in (False, True):
            with self.subTest(ordinary_error=ordinary_error), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                home = root / 'home'; home.mkdir()
                model = root / 'model-sandbox'; model.mkdir()
                config = home / 'config.toml'
                original = (b'default_permissions = "existing"\nmodel = "retained-model"\n'
                            b'[permissions.existing.filesystem]\n":root" = "deny"\n":minimal" = "read"\n')
                config.write_bytes(original); config.chmod(0o600)
                try:
                    with ExitStack() as lifetime:
                        native_adapter.prepare_r1_permissions(home, model, [root / 'old-fixture'], lifetime)
                        actual = tomllib.loads(config.read_text())
                        self.assertEqual(actual['default_permissions'], 'existing')
                        self.assertEqual(actual['model'], 'retained-model')
                        profile = actual['permissions'][native_adapter.QUALIFICATION_PERMISSION_PROFILE]
                        self.assertEqual(profile['filesystem'][':root'], 'deny')
                        self.assertEqual(profile['filesystem'][str((root / 'old-fixture').resolve())], 'deny')
                        self.assertEqual(profile['filesystem'][str(model.resolve())], 'write')
                        self.assertFalse(profile['network']['enabled'])
                        if ordinary_error:
                            raise ValueError('ordinary launch setup failure')
                except ValueError:
                    if not ordinary_error:
                        raise
                self.assertEqual(config.read_bytes(), original)
                self.assertEqual(config.stat().st_mode & 0o777, 0o600)

    def test_initial_native_context_and_argv_stay_inside_new_sample(self):
        from adapters.eval.test_native_constraint_transport import request as native_request
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request = native_request(root, PACKAGE.name, 'native-implementation-plan-premise')
            values = native_adapter.build_context(request, 'codex')
            try:
                protocol = json.loads(values[4].read_text())
                self.assertIn(request['prompt'], values[0])
                self.assertEqual(values[1].read_text(), values[0])
                model = root / 'execution/model-sandbox'
                self.assertEqual(Path(protocol['model_root']), model.resolve())
                self.assertEqual(protocol['implementation_context_id'], implementation_authoring.ENTRY_CONTEXT)
                self.assertIsNone(protocol['architecture_context'])
                self.assertFalse(list((Path(protocol['owner_repository']) / '.trellis/tasks').glob('*/task.json')))
                request['_model_root'] = str(model)
                argv, _ = native_adapter.native_argv('codex', 'codex', request, values[0], values[1], values[5],
                                                     Path(protocol['projection_root']))
                self.assertEqual(argv[-1], values[0])
                self.assertIn('default_permissions=' + json.dumps(native_adapter.QUALIFICATION_PERMISSION_PROFILE), argv)
                self.assertIn('shell_environment_policy.set.TMPDIR=' + json.dumps(str(model / 'output')), argv)
                self.assertNotIn('resume', argv)
            finally:
                values[9].set(); values[8].join(timeout=2)


if __name__ == '__main__':
    unittest.main()
