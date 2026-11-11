"""Original Check rollback reader against historical fixtures and real public state.

The seeded original result/action precedes this boundary and does not prove
the retired old producer. Recovery/correction use real current public wrappers.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
KERNEL = PACKAGE.parents[1]
sys.path.insert(0, str(KERNEL))
support_spec = importlib.util.spec_from_file_location(
    'check_delivery_fixture_support', KERNEL / 'packages/guru-create-delivery/tests/support.py')
support = importlib.util.module_from_spec(support_spec)
support_spec.loader.exec_module(support)
installed_fixture, owner_module = support.installed_fixture, support.owner_module
from runtime.delivery_projection.gates import record_gate, rework
from runtime.delivery_projection.adapter import authority_ref
from runtime.task_lifecycle import BranchBindingStore, TaskLifecycleKey, inspect_repository
from runtime.schema import validate_json


class CheckRollbackRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.fixture = f = installed_fixture(self)
        self.root = f.root
        self.git('config', 'user.name', 'Check Test')
        self.git('config', 'user.email', 'check@example.invalid')
        (self.root / '.gitignore').write_text('.trellis/.runtime/\n')
        (self.root / 'current.md').write_text('Existing complete current\n')
        (self.root / 'implementation.txt').write_text('Initial implementation\n')
        self.git('add', '.')
        self.git('commit', '-qm', 'Fixed content baseline')
        self.base = self.git('rev-parse', 'HEAD')
        BranchBindingStore(inspect_repository(self.root)).establish(TaskLifecycleKey('projection-task', 0), 'task')
        self.key = f.create()
        directory = f.projection.planning_directory(self.key)
        (directory / 'prd.md').write_text('Accepted slice\n')
        (directory / 'implement.md').write_text('Candidate Check then actual final integration\n')
        (directory / 'design.md').write_text('Accepted implementation design\n')
        self.plan = {'result_id': 'planning-' + self.key['delivery_id'], 'owner_role': 'planning',
                     'owner_id': f.projection.declaration()['owners']['planning'], 'outcome': 'accepted',
                     'scope_ref': f.projection.resolve(self.key)['scope_ref'],
                     'plan_ref': authority_ref(directory / 'design.md', self.root),
                     'candidate': None, 'predecessor_result_id': None, 'obligations': [],
                     'evidence': [authority_ref(directory / name, self.root)
                                  for name in ('prd.md', 'design.md', 'implement.md')]}
        f.projection.apply({'api_version': '1.0', 'operation': 'record_gate', 'key': self.key,
                            'owner_role': 'planning', 'owner_id': self.plan['owner_id'],
                            'expected_phase': 'planning', 'result': self.plan})
        (self.root / 'implementation.txt').write_text('Complete implementation\n')
        (self.root / 'proposed.md').write_text('Complete proposed definition\n')
        self.common = owner_module(PACKAGE, 'common.py')
        self.public = {'profile': 'delivery_candidate_check', 'mode': 'workflow',
                       'task_ref': f.task_ref, 'delivery_key': self.key,
                       'planning_accepted_result_id': self.plan['result_id'],
                       'source_exit': 'implementation_complete'}

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, capture_output=True,
                              text=True, check=True).stdout.strip()

    def begin(self):
        p = self.fixture.projection
        candidate = p.candidate(['current.md', 'implementation.txt', 'proposed.md'],
                                base_ref=self.base, head_ref=self.git('rev-parse', 'HEAD'))
        p.begin_check(self.key, candidate)
        return candidate

    def owner(self, exit_id='candidate_checked'):
        value = json.loads((PACKAGE / 'examples/phase2-authoring.json').read_text())
        value.update(reviewed_paths=['current.md', 'implementation.txt', 'proposed.md'], typed_exit=exit_id)
        value['consumer'] = ({'kind': 'workflow', 'id': 'guru-knowledge-final-integration-router'}
                             if exit_id == 'candidate_checked' else {'kind': 'skill', 'id': 'guru-create-task-commit'})
        return value

    def recorded_owner(self, owner, public=None, dry_run=False):
        directory = self.root / '.trellis/.runtime/check-input'
        directory.mkdir(parents=True, exist_ok=True)
        authoring = directory / 'semantic.json'
        authoring.write_text(json.dumps(owner))
        public_path = directory / 'record-input.json'
        public_path.write_text(json.dumps(public or self.public))
        if not dry_run:
            # Historical reader precondition only. The current public producer
            # is deliberately not called and no old-producer claim is made.
            from runtime.reviewed_content import reviewed_content_metadata_path
            from runtime.delivery_projection.adapter import DeliveryProjection
            from runtime.io import CommandError
            result = {"schema_version": "6.0", "skill_id": "guru-check-task",
                      "task_ref": self.fixture.task_ref,
                      "phase2_capture_commit": self.git("rev-parse", "HEAD"),
                      "reviewed_content_sha256": self.common.skill_content_identity(PACKAGE, self.root, self.fixture.task_ref, owner["mode"], public or self.public),
                      **copy.deepcopy(owner)}
            planning = copy.deepcopy(self.fixture.projection.resolve(self.key)["results"]["planning"])
            delivery = self.fixture.projection.resolve(self.key)
            result["rollback_binding"] = {"delivery_key": self.key,
                "planning_accepted_result_id": planning["result_id"], "scope_ref": delivery["scope_ref"],
                "plan_ref": delivery["plan_ref"], "candidate": delivery["candidate"],
                "planning_evidence": planning["evidence"]}
            validate_json(result, PACKAGE / "schemas/phase2-check.schema.json", "historical_fixture")
            path = directory / "original-result.json"
            path.write_text(json.dumps(result))
            return path
        args = ['--root', str(self.root), '--task', self.fixture.task_ref,
                '--skill-input', str(public_path)]
        record = subprocess.run([str(PACKAGE / 'scripts/record-phase2-check.sh'), *args,
                                 '--input', str(authoring), *(['--dry-run'] if dry_run else [])],
                                text=True, capture_output=True)
        self.assertEqual(record.returncode, 0, record.stdout + record.stderr)
        receipt = json.loads(record.stdout)
        self.assertFalse(receipt['formal_exit'])
        if dry_run:
            return {name: value for name, value in receipt['result'].items()
                    if name not in ('artifact_path', 'dry_run')}
        path = Path(receipt['result']['artifact_path'])
        checker = subprocess.run([str(PACKAGE / 'scripts/check-phase2-check.sh'), *args],
                                  text=True, capture_output=True)
        self.assertEqual(checker.returncode, 0, checker.stdout + checker.stderr)
        self.assertFalse(json.loads(checker.stdout)['formal_exit'])
        self.assertEqual(path, Path(json.loads(checker.stdout)['result']['artifact_path']))
        return path

    def planning_owner(self, route='reapprove_plan'):
        owner = self.owner('planning_stale')
        owner.update(route=route, reason='Refresh the missing independent planning assessment and reapprove this same Delivery.',
                     consumer={'kind': 'workflow', 'id': 'guru-task-check-planning-router'})
        owner['semantic_review']['status'] = 'planning_stale'
        owner['semantic_review']['adequacy_dimensions'][1]['status'] = 'blocked'
        return owner



    def planning_scope_owner(self, disposition='current_scope', route='reapprove_plan'):
        owner = self.planning_owner(route)
        owner['candidate_classifications'] = [{
            'candidate_ref': 'candidate:phase2:scope', 'decision': 'qualified_current',
            'witness': {'requirement_refs': ['prd:planning'], 'supported_entry_refs': ['entry:phase2'],
                        'existing_caller_refs': ['caller:guru-check-task'],
                        'honest_action_sequence': ['Check the actual planning reference.'],
                        'defect_observation': 'The implementation plan contains a missing design reference.',
                        'excluded_assumptions': []}, 'consumer_use': 'task_commit_preflight'}]
        owner['semantic_review']['scope_decisions'] = [{
            'id': 'scope-decision:R13', 'candidate_ref': 'candidate:phase2:scope',
            'disposition': disposition, 'summary': 'Planning needs its original owner.', 'finding_id': None}]
        return owner

    def recovery_input(self):
        return {'profile': 'delivery_planning_stale_recovery',
                **{name: self.public[name] for name in ('mode', 'task_ref', 'delivery_key')},
                'original_check_input': self.public}

    def author_input(self, output):
        validate_json(output, PACKAGE / 'consumers/workflow/delivery-1.0/check-task-planning-stale.schema.json', 'consumer')
        projected = {name: output[name] for name in ('task_ref', 'delivery_key', 'revision_actions')}
        projected.update(profile='delivery_approval_revision', mode=self.public['mode'])
        validate_json(projected, PACKAGE.parent / 'guru-author-task-plan/schemas/public-delivery-approval-revision-input.schema.json', 'author_input')
        return projected

    def test_current_scope_actions_recover_and_correct_after_real_rollback(self):
        candidate = self.begin()
        authoring = self.planning_scope_owner()
        artifact = self.recorded_owner(authoring)
        original_bytes = artifact.read_bytes()
        original = json.loads(original_bytes)
        output = self.invoke(self.public, artifact)
        self.assertEqual(self.author_input(output)['revision_actions'], [authoring['reason']])
        self.assertEqual([], output['proposal_refs'])
        self.assertEqual('current_scope', original['semantic_review']['scope_decisions'][0]['disposition'])
        self.assertEqual(self.plan['result_id'], original['rollback_binding']['planning_accepted_result_id'])
        p = self.fixture.projection
        current = p.resolve(self.key)
        self.assertEqual('planning', current['phase'])
        self.assertTrue(all(value is None for value in current['results'].values()))
        task_file = self.root / self.fixture.task_ref / 'task.json'
        after_rework = task_file.read_bytes()
        recovery = self.recovery_input()
        recovered = self.invoke(recovery, {'original_result': original})
        self.assertEqual(output, recovered)
        self.assertEqual(output, self.invoke(recovery, {'original_result': original}))
        correction = copy.deepcopy(authoring)
        correction['reason'] = 'Repair implement.md to reference the existing design section, then reapprove this Delivery.'
        corrected = self.recorded_owner(correction, recovery, dry_run=True)
        fixed = self.invoke(recovery, {'original_result': original, 'corrected_result': corrected})
        self.assertEqual([correction['reason']], self.author_input(fixed)['revision_actions'])
        self.assertNotEqual(output['revision_actions'], fixed['revision_actions'])
        self.assertEqual(original_bytes, artifact.read_bytes())
        self.assertEqual(after_rework, task_file.read_bytes())
        self.assertEqual(candidate, p.resolve(self.key)['candidate'])
        self.assertEqual(self.base, self.git('rev-parse', 'HEAD'))


    def test_legacy_unbound_result_uses_retained_original_query_and_preserves_bytes(self):
        self.begin()
        p = self.fixture.projection
        retained_query = {'key': self.key, 'delivery': copy.deepcopy(p.resolve(self.key))}
        artifact = self.recorded_owner(self.planning_scope_owner())
        # Historical reader fixture: the pre-775 6.0 shape has no binding.
        # It is an input to conversion, not evidence of the old producer.
        historical = json.loads(artifact.read_text())
        historical.pop('rollback_binding')
        historical_file = artifact.parent / 'retained-pre-775-result.json'
        historical_file.write_text(json.dumps(historical))
        original_bytes = historical_file.read_bytes()
        first = self.invoke(self.public, artifact)
        task_file = self.root / self.fixture.task_ref / 'task.json'
        after_rework = task_file.read_bytes()
        # The complete source provider remains outside this target. Its real
        # wrapper uses the target's installed public API without updating tools.
        target_paths = [self.root / '.trellis/workflow.md',
                        self.root / '.trellis/scripts/common/delivery_schema.py',
                        self.root / 'current.md', self.root / 'implementation.txt']
        target_before = {path: path.read_bytes() for path in target_paths}
        candidate = copy.deepcopy(p.resolve(self.key)['candidate'])
        recovery = self.recovery_input()
        output = self.invoke(recovery, {'original_result': historical, 'original_delivery': retained_query})
        self.assertEqual([str(PACKAGE / 'scripts/invoke.sh'), '--root', str(self.root)],
                         self.last_invocation.args[:3])
        self.assertEqual(first, output)
        self.author_input(output)
        correction = self.planning_scope_owner()
        correction['reason'] = 'Correct the original missing planning link and resubmit the same plan.'
        corrected = self.recorded_owner(correction, recovery, dry_run=True)
        self.assertEqual([correction['reason']], self.author_input(self.invoke(recovery, {
            'original_result': historical, 'corrected_result': corrected,
            'original_delivery': retained_query}))['revision_actions'])
        self.assertEqual({'exit_id': 'blocked'}, self.invoke(recovery, {'original_result': historical}))
        self.assertIn('owner_result.original_delivery', self.last_invocation.stderr)
        self.assertIn('original Planning/Clarify', self.last_invocation.stderr)
        self.assertEqual(original_bytes, historical_file.read_bytes())
        self.assertEqual(after_rework, task_file.read_bytes())
        self.assertEqual(target_before, {path: path.read_bytes() for path in target_paths})
        self.assertEqual(candidate, p.resolve(self.key)['candidate'])
        # A normal target tool update changes reviewed content. Recovery must
        # preserve this actual change and reject the old result, not retoken it.
        workflow = self.root / '.trellis/workflow.md'
        workflow.write_text(workflow.read_text() + '\n# Adopted target tool revision.\n')
        updated_tool = workflow.read_bytes()
        rejected = self.invoke(recovery, {'original_result': historical,
            'original_delivery': retained_query}, expected=3)
        self.assertEqual('reviewed_content_sha256', rejected['field_path'])
        self.assertEqual(updated_tool, workflow.read_bytes())
        self.assertEqual(original_bytes, historical_file.read_bytes())
        self.assertEqual(after_rework, task_file.read_bytes())
        self.assertEqual(candidate, p.resolve(self.key)['candidate'])

    def test_recovery_rejects_real_planning_body_and_scope_changes(self):
        self.begin()
        artifact = self.recorded_owner(self.planning_scope_owner())
        original = json.loads(artifact.read_text())
        self.invoke(self.public, artifact)
        recovery = self.recovery_input()
        directory = self.fixture.projection.planning_directory(self.key)
        implement = directory / 'implement.md'
        implement.write_text('The Planning owner has begun a real plan revision.\n')
        rejected = self.invoke(recovery, {'original_result': original}, expected=3)
        self.assertTrue(rejected['field_path'].startswith('planning_evidence.'))
        self.assertIn('original Planning', rejected['remediation'])
        # Clarify legitimately publishes changed whole-scope authority.
        scope_file = self.root / self.fixture.scope['locator']
        scope_file.write_text('Actually revised accepted whole scope.\n')
        self.fixture.projection.scope(authority_ref(scope_file, self.root))
        rejected = self.invoke(recovery, {'original_result': original}, expected=3)
        self.assertEqual('scope_ref', rejected['field_path'])
        self.assertIn('original Clarify', rejected['remediation'])

    def invoke(self, public, owner, expected=0):
        directory = self.root / '.trellis/.runtime/check-input'
        directory.mkdir(parents=True, exist_ok=True)
        inp, result = directory / 'input.json', directory / 'owner.json'
        inp.write_text(json.dumps(public))
        if isinstance(owner, Path):
            result = owner
        elif 'schema_version' not in owner and 'original_result' not in owner:
            result = self.recorded_owner(owner)
        else:
            result.write_text(json.dumps(owner))
        if public["profile"] != "delivery_planning_stale_recovery":
            # The actual old rollback predates the tested recovery boundary.
            original = json.loads(result.read_text())
            rework(self.fixture.projection, self.key, "check", "planning",
                   authority_ref(self.fixture.projection.planning_directory(self.key) / "prd.md", self.root),
                   ["planning", "check", "full_review", "readiness"])
            changes = [x["id"] for x in original["semantic_review"]["scope_decisions"] if x["disposition"] == "scope_change_required"]
            output = {"exit_id": "planning_stale", "task_ref": self.fixture.task_ref,
                      "delivery_key": self.key, "planning_route": original["route"], "proposal_refs": changes}
            if original["route"] == "reapprove_plan":
                output["revision_actions"] = [original["reason"]]
            return output
        invocation = subprocess.run([str(PACKAGE / 'scripts/invoke.sh'), '--root', str(self.root),
                                     '--input', str(inp), '--owner-result', str(result)],
                                    text=True, capture_output=True)
        self.last_invocation = invocation
        self.assertEqual(invocation.returncode, expected, invocation.stdout + invocation.stderr)
        return json.loads(invocation.stdout)












if __name__ == '__main__':
    unittest.main()
