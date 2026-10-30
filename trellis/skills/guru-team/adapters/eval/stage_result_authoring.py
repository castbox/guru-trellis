"""Fact-only current-API stage-result fixtures and original command transport.

Historical gates establish isolated entry preconditions. They are never native
review evidence. The current native worker authors every tested judgment.
"""
from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from adapters.eval import implementation_authoring as implementation
from adapters.eval import phase2_authoring as phase2
from adapters.eval.fixture_io import run_git
from adapters.eval.phase2_authoring import write_json

FACTS = '.trellis/tasks/stage-result-evidence/facts.json'
PUBLIC_INPUT = '.trellis/tasks/stage-result-evidence/input.json'
PUBLIC_READS = ('SKILL.md', 'interface.json', 'commands.json')
REASONING = '.trellis/tasks/stage-result-evidence/current-review.md'
ARCHITECTURE_PREREQUISITE = '.trellis/tasks/stage-result-evidence/architecture-prerequisite.json'
CONSUMED_INTERMEDIATE_INPUTS = {
    ('guru-review-branch', 'review-branch'): ('--semantic-review-file',),
    ('guru-check-task', 'record-phase2-check'): ('--input',),
    ('guru-create-task-commit', 'prepare-task-commit'): ('--input', '--candidate-json'),
    ('delivery-api', 'begin-check'): ('--input',),
    ('delivery-api', 'rework'): ('--input',),
}


def facts_locator(request: dict) -> str:
    return FACTS


def owner_schema(package: Path) -> str:
    return ('schemas/semantic-result.schema.json' if package.name == 'guru-review-task-delivery'
            else 'schemas/semantic-delivery-result-1.0.schema.json')


def public_reads(package):
    contract = ("references/contract.md",) if (package / "references/contract.md").is_file() else ()
    return (*PUBLIC_READS, *contract, owner_schema(package))


class ImplementationCommands(implementation.ImplementationCommands):
    owners = (*implementation.OWNERS, 'guru-review-task-delivery',
              'guru-review-task-completion', 'guru-review-branch',
              'guru-create-task-commit', 'guru-publish-task-delivery',
              'guru-merge-task-delivery')

    def __init__(self, repository, environment, receipts_path, *, facts_relative=FACTS):
        facts = json.loads((repository / facts_relative).read_text())
        if facts.get('continuous_chain'):
            environment = {**environment, 'PATH': facts['provider_bin'] + os.pathsep + environment['PATH']}
        super().__init__(repository, environment, receipts_path, facts_relative=facts_relative)
        self.consumed_paths = set()

    def _file_argument(self, arguments, flag):
        if flag not in arguments or arguments.index(flag) + 1 == len(arguments):
            return None
        value = arguments[arguments.index(flag) + 1]
        if value == '-' or value.lstrip().startswith(('{', '[')):
            return None
        path = Path(value)
        return (path if path.is_absolute() else self.repository / path).resolve()

    def _retire_input(self, path):
        runtime = (self.repository / '.trellis/.runtime/guru-team/evals').resolve()
        if path is not None and path.parent == runtime:
            path.unlink(missing_ok=True)
            self.consumed_paths.add(path.relative_to(self.repository.resolve()).as_posix())

    def _retire_planning_recorder_input(self, payload, facts):
        if payload['skill_id'] != 'guru-approve-task-plan':
            return
        checkpoint = self._file_argument(payload['arguments'], '--owner-result')
        if checkpoint is None:
            return
        preceding = []
        if facts.get('continuation_locator'):
            continuation = json.loads((self.repository / facts['continuation_locator']).read_text())
            preceding = continuation['preceding_commands']
        # Only the latest actual writer of this consumed checkpoint identifies
        # its input. Existing continuation receipts cover a resumed invocation.
        for receipt in reversed([*preceding, *self.receipts]):
            request, response = receipt['request'], receipt['response']
            if (request['skill_id'] != payload['skill_id']
                    or request['command'] != 'record-planning-approval' or response['returncode']):
                continue
            try:
                recorded = json.loads(response['stdout'])['result']
            except (ValueError, KeyError, TypeError):
                continue
            artifact = recorded.get('artifact_path')
            if (not isinstance(artifact, str) or recorded.get('dry_run')
                    or self._file_argument(['--artifact', artifact], '--artifact') != checkpoint):
                continue
            self._retire_input(self._file_argument(request['arguments'], '--input'))
            break

    def forward(self, payload):
        facts = json.loads((self.repository / self.facts_relative).read_text())
        if payload['skill_id'] == 'implementation-authoring' and payload['command'] == 'write':
            try:
                supplied = json.loads(payload.get('stdin') or '')
                updates = supplied['file_updates']
                if not isinstance(updates, dict) or not all(
                        isinstance(path, str) and isinstance(content, str)
                        for path, content in updates.items()):
                    raise ValueError('write requires file_updates mapping paths to complete text')
            except (ValueError, KeyError, TypeError) as error:
                result = {'returncode': 0, 'stdout': json.dumps({'request_error': str(error),
                    'returncode': 2, 'stdout': '', 'stderr': 'Supply write stdin as JSON {file_updates:{path:text}}.'}) + '\n', 'stderr': ''}
                self.record_response(payload, result)
                return result
        if not self.terminal and facts.get('continuous_chain'):
            if payload['skill_id'] == 'implementation-authoring' and payload['command'] == 'write':
                from runtime.delivery_projection.adapter import DeliveryProjection
                record = DeliveryProjection(self.repository, facts['task_ref']).read_record()
                planning_paths = {facts['task_ref'] + '/' + row['planning_root'] + '/' + name
                    for row in record['deliveries']
                    for name in ('prd.md', 'design.md', 'implement.md', 'implement.jsonl', 'check.jsonl')}
                contribution = facts.get('contribution_locator',
                    'docs/requirements-design-test-contributions/stage-chain')
                updates = json.loads(payload['stdin'])['file_updates']
                for relative in updates:
                    path = Path(relative)
                    if path.is_absolute() or '..' in path.parts or not (
                            relative in facts['writable_paths'] or relative in planning_paths
                            or path.is_relative_to(contribution)):
                        result = {'returncode': 0, 'stdout': json.dumps({
                            'request_error': 'continuous authoring write is outside its actual Task targets',
                            'returncode': 2, 'stdout': '',
                            'stderr': 'Use run for transient original-wrapper JSON under .trellis/.runtime/guru-team/evals; write accepts only the supplied Task targets.'}) + '\n', 'stderr': ''}
                        self.record_response(payload, result)
                        return result
                for relative, content in updates.items():
                    target = self.repository / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(content)
                result = {'returncode': 0, 'stdout': json.dumps({'written_paths': list(updates)}) + '\n', 'stderr': ''}
                self.record_response(payload, result)
                return result
            if payload['skill_id'] == 'implementation-authoring' and payload['command'] == 'inspect':
                from runtime.delivery_projection.adapter import DeliveryProjection
                from runtime.reviewed_content import reviewed_content_identity
                observed = {'head': run_git(self.repository, 'rev-parse', 'HEAD'),
                    'task': DeliveryProjection(self.repository, facts['task_ref']).read_record(),
                    'status': run_git(self.repository, 'status', '--short'),
                    'diff': run_git(self.repository, 'diff', facts['initial_head']),
                    'content_identity': 'sha256:' + reviewed_content_identity(self.repository)['sha256']}
                result = {'returncode': 0, 'stdout': json.dumps(observed) + '\n', 'stderr': ''}
                self.record_response(payload, result)
                return result
            if payload['skill_id'] == 'guru-maintain-architecture-baseline':
                # Project actual newly authored files for the fresh independent
                # reader. The projection contains no judgment or private state.
                import shutil
                from adapters.eval.eval_support import repository_projection_allowed
                target = self.projection_repository
                for path in self.repository.rglob('*'):
                    relative = path.relative_to(self.repository)
                    if not path.is_file() or not repository_projection_allowed(relative):
                        continue
                    destination = target / relative
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    if not destination.exists():
                        shutil.copy2(path, destination)
                    elif not os.path.samefile(path, destination):
                        destination.write_bytes(path.read_bytes())
        try:
            result = super().forward(payload)
        except (ValueError, KeyError, TypeError) as error:
            # Request syntax/undeclared commands execute no original wrapper.
            # Preserve that ordinary error and let the native caller read help.
            # A real original-wrapper failure still returns nonzero and stops.
            result = {'returncode': 0, 'stdout': json.dumps({'request_error': str(error),
                'returncode': 2, 'stdout': '', 'stderr': 'Read the exact owner command contract through run, then correct this request.'}) + '\n', 'stderr': ''}
            self.record_response(payload, result)
            return result
        # A zero process exit can still carry a transport request error.
        # Only an actual completed consumer may retire its file arguments.
        try:
            output = json.loads(result['stdout'])
        except ValueError:
            output = None
        consumed = (result['returncode'] == 0 and isinstance(output, dict)
                    and 'request_error' not in output and output.get('returncode', 0) == 0)
        arguments = payload['arguments']
        if consumed and not any(flag in arguments for flag in ('--help', '--dry-run')):
            for flag in CONSUMED_INTERMEDIATE_INPUTS.get(
                    (payload['skill_id'], payload['command']), ()):
                self._retire_input(self._file_argument(arguments, flag))
        # Inputs shared with a public invocation remain until that invocation
        # succeeds. Planning recorder inputs use their existing checkpoint link.
        public_invocation = payload['command'] in {'invoke', 'invoke-' + payload['skill_id']}
        if consumed and payload['skill_id'] in self.owners and public_invocation:
            self._retire_planning_recorder_input(payload, facts)
            for flag in ('--input', '--semantic-result', '--owner-result', '--review-input', '--invocation'):
                self._retire_input(self._file_argument(arguments, flag))
        return result


validate_trace = implementation.validate_trace


def stage_architecture_prerequisite(fixture, check, *, completion):
    """Supply the original wrapper's isolated entry fact, not native coverage."""
    from runtime.reviewed_content import reviewed_content_identity
    public = json.loads((fixture / phase2.ARCHITECTURE_INPUT).read_text())
    public.update(schema_version='5.0' if completion else 'delivery-3.0',
                  profile='task_impact_sync' if completion else 'delivery_task_impact_sync',
                  source_exit='acceptance_finish' if completion else 'review_passed',
                  stage='acceptance_finish' if completion else 'publication',
                  continuation_id='historical-stage-entry')
    if completion:
        public.pop('delivery_key', None)
        public.pop('planning_root', None)
    public['project_contract']['guru_contract_identity'] = 'guru-maintain-architecture-baseline:5.0'
    public['candidate']['head'] = run_git(fixture, 'rev-parse', 'HEAD')
    public['candidate']['content_identity'] = 'sha256:' + reviewed_content_identity(fixture)['sha256']
    fields = ('schema_version', 'profile', 'source_exit', 'mode', 'continuation_id', 'stage',
              'task_locator', 'baseline', 'constitution', 'project_contract', 'freshness_identity',
              'before_authority', 'candidate', 'delivery_key', 'planning_root')
    owner = {name: public[name] for name in fields if name in public and name != 'source_exit'}
    owner.update(input_sha256=hashlib.sha256(json.dumps(public, ensure_ascii=False,
        sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        baseline_identity=public['baseline']['identity'],
        constitution_identity=public['constitution']['identity'],
        impact_kind='no_architecture_impact', promotion_state='no_change',
        impact_reason='Historical isolated entry prerequisite for the existing predicate/filter boundary; not native assessment evidence.',
        typed_exit='baseline_current',
        consumer={'kind': 'workflow', 'id': 'guru-architecture-baseline-current-router'},
        ai_review_gate={'status': 'passed', 'reviewed_scope': 'Fixture-owned historical entry prerequisite only.',
            'evidence_summary': 'The original wrapper binds this test prerequisite to actual source and candidate. No current native Architecture judgment is claimed.',
            'findings': [], 'conclusion': 'Historical isolated entry fact only.'})
    package = fixture / '.trellis/guru-team/skills/packages/guru-maintain-architecture-baseline'
    result = subprocess.run([str(package / 'scripts/invoke.sh'), '--invocation',
        json.dumps({'public_input': public, 'owner_result': owner})],
        cwd=fixture, capture_output=True, text=True)
    if result.returncode:
        raise ValueError('Architecture entry prerequisite failed: ' + result.stdout + result.stderr)
    write_json(fixture / ARCHITECTURE_PREREQUISITE, {'seed_boundary':
        'Original-wrapper historical prerequisite only; not native or continuous-chain proof.',
        'public_input': public, 'result': json.loads(result.stdout)})


def _seed(request, fixture, source_repo, *, additional=None, candidate=None, scope='', filter_pending=False):
    """Use real installed Task creation, Delivery creation and activation APIs."""
    bodies = implementation._code_drift_seed_bodies()
    authority = implementation._implementation_range_authority('native-implementation-code-drift')
    if filter_pending:
        # This case starts with two missing function bodies. Its planning and
        # historical source observations must describe that same starting point.
        replacements = {
            'predicate stub, existing filter, four tests': 'predicate and filter stubs, four tests',
            'unimplemented predicate, existing filter and four existing tests':
                'unimplemented predicate and filter, and four existing tests',
            'interval.py is the implementation difference':
                'interval.py and range_filter.py are the implementation differences',
            'range_filter.select already composes it to filter values. The missing predicate prevents that caller from returning the documented members.':
                'range_filter.select is also an unconnected stub. Both bodies must implement the documented membership and filtering behavior.',
            'replace the missing inclusive predicate and verify the existing filter caller':
                'implement the inclusive predicate and connect the missing filter caller',
            'range_filter.py already uses a list comprehension over contains.':
                'range_filter.py is an unconnected stub with the required select signature.',
            'Replace the predicate body with inclusive comparisons. Keep the filter, signatures and supported input domain unchanged.':
                'Implement inclusive comparisons in the predicate and connect select through a predicate-based list comprehension. Keep signatures and the supported input domain unchanged.',
            'range_filter.select retains its existing predicate-based list comprehension':
                'range_filter.select must implement a predicate-based list comprehension',
            'implement lower <= value <= upper in interval.contains. Preserve signatures, purity, filter composition and existing valid assertions.':
                'implement lower <= value <= upper in interval.contains and connect range_filter.select to that predicate. Preserve signatures, purity, order, duplicates and existing valid assertions.',
            'its existing composition': 'its required predicate composition',
            'using integer comparisons.\nrange_filter.py:select composes contains in its existing list comprehension':
                'using integer comparisons.\nrange_filter.py:select must compose contains in a list comprehension',
            'stub raising NotImplementedError and the existing range_filter.select comprehension.':
                'stub and an unconnected range_filter.select stub, both raising NotImplementedError.',
        }
        for old, new in replacements.items():
            bodies = {name: body.replace(old, new) for name, body in bodies.items()}
            authority = authority.replace(old, new)
    if scope:
        bodies['task-prd.md'] += '\n' + scope + '\n'
        bodies['task-prd.md'] = bodies['task-prd.md'].replace('No external service or predecessor Delivery is required.', 'R1 requires no external service or predecessor Delivery. R2 below owns its separate conditions.').replace('new APIs, migration or deployment work.', 'unrequested APIs, migration or deployment changes. R2 below defines any required external observation.')
        bodies['prd.md'] += '\nThis source slice covers R1 only. The additional whole-Task R2 is excluded from this historical Delivery and remains for its original owner.\n'
        bodies['implement.md'] = bodies['implement.md'].replace('Policy: full. D1 covers all accepted R1 and AC1..AC3, with no deferred scope or later stage.', 'Policy: partial. D1 covers R1 and AC1..AC3. The additional whole-Task R2 remains with implementation or the named external evidence owner, according to its actual requirement. Whole Task Completion requires both requirements.')
    with tempfile.TemporaryDirectory(prefix='stage-result-source-') as temporary:
        path = Path(temporary)
        write_json(path / 'input.json', {'profile': 'delivery_initial_check', 'mode': 'workflow',
                                        'task_ref': '.trellis/tasks/current'})
        (path / 'interval.py').write_text('def contains(value, lower, upper):\n    return lower <= value <= upper\n')
        phase2.stage({**request, 'case_id': 'native-owner-clean', 'workdir': temporary,
                      'files': ['input.json', 'interval.py']}, fixture,
                     fixture / '.trellis/guru-team/skills/packages/guru-check-task', source_repo,
                     seed_bodies=bodies,
                     range_authority_body=authority,
                     fixture_files=additional, candidate_files=candidate)


def stage_check(request, fixture, package, source_repo):
    case = request['case_id']
    additional = {'docs/prior-slice.md': '# Earlier slice observation\n\nAt P1 cutoff only the predicate was available. CLI/filter guidance was deferred until the inclusive production filter was implemented and tested. P2 implementation and original RDT owners own that release. This is a historical observation, not a current restriction.\n'}
    candidate = {}
    if case.endswith('c01'):
        additional['docs/current-usage.md'] = '# Current usage\n\nThe filter is unavailable. Call the predicate directly.\n'
    else:
        additional['docs/current-usage.md'] = '# Current usage\n\nUse range_filter.select for inclusive filtering; there is no current deployment or enablement prerequisite for this pure local function.\n'
    if case.endswith('c02'):
        candidate['test_interval.py'] = ('import unittest\nfrom interval import contains\nclass IntervalTests(unittest.TestCase):\n'
            '    def test_stage_assertion(self):\n        self.assertTrue(contains(2,2,4))\n'
            '    @unittest.skip("P1: filter unavailable")\n'
            '    def test_filter(self):\n        from range_filter import select\n        self.assertEqual(select([1,2,3,4,5],2,4), [])\n')
    if case.endswith('c03'):
        additional['range_filter.py'] = 'from interval import contains\ndef select(values, lower, upper):\n    raise NotImplementedError("filter consumer not connected")\n'
        additional['docs/current-usage.md'] = '# Current usage\n\nThe inclusive filter is required by the current contract. Its consumer has not yet been connected; no deployment or enablement prerequisite applies to this pure local function.\n'
    _seed(request, fixture, source_repo, additional=additional, candidate=candidate,
          filter_pending=case.endswith('c03'))
    # Include actual current consumer observations, not an expected route.
    argv = [sys.executable, '-B', '-c', 'from range_filter import select; print(select([1,2,3,4,5],2,4))']
    result = subprocess.run(argv, cwd=fixture, capture_output=True, text=True)
    additional_argv = [sys.executable, '-B', '-c',
        'from range_filter import select; '
        'assert select([1,2,3],2,2)==[2]; '
        'assert select([4,2,4,1,3],2,4)==[4,2,4,3]; '
        'print("singleton and duplicate/order probes passed")']
    additional_result = subprocess.run(additional_argv, cwd=fixture, capture_output=True, text=True)
    write_json(fixture / 'docs/phase2-evidence/consumer-observation.json', {
        'argv': argv, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
        'additional_probes': {'argv': additional_argv, 'returncode': additional_result.returncode,
            'stdout': additional_result.stdout, 'stderr': additional_result.stderr}})
    facts = json.loads((fixture / phase2.FACTS).read_text())
    facts['required_reads'] += ['docs/phase2-evidence/consumer-observation.json']
    facts['reviewed_paths'] = sorted(set([*facts['reviewed_paths'],
        'docs/phase2-evidence/consumer-observation.json']))
    facts['architecture_reads'] += ['docs/current-usage.md', 'docs/prior-slice.md', 'test_interval.py']
    write_json(fixture / phase2.FACTS, facts)
    # Bind Architecture to the actual candidate after adding its observation.
    from runtime.reviewed_content import reviewed_content_identity
    architecture = json.loads((fixture / phase2.ARCHITECTURE_INPUT).read_text())
    architecture['candidate']['content_identity'] = 'sha256:' + reviewed_content_identity(fixture)['sha256']
    write_json(fixture / phase2.ARCHITECTURE_INPUT, architecture)
    facts['architecture_input_sha256'] = hashlib.sha256(json.dumps(
        architecture, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    write_json(fixture / phase2.FACTS, facts)


def stage(request, fixture, package, source_repo):
    from adapters.eval import stage_result_chain
    if request['case_id'] == stage_result_chain.CASE:
        return stage_result_chain.stage(request, fixture, package, source_repo)
    from adapters.eval.planning_authoring import acquire_authoring_checkout, register_authoring_resources
    from runtime.delivery_projection.adapter import DeliveryProjection, authority_ref
    from runtime.delivery_projection.gates import record_gate, rework
    from runtime.reviewed_content import reviewed_content_metadata_path
    acquisition = acquire_authoring_checkout(fixture, branch_name='eval/stage-result')
    case = request['case_id']
    completion = package.name == 'guru-review-task-completion'
    policy = ('The selected slice delivers the pure inclusive predicate and filter source. '
              'Control is not open in this fixture environment. Initialization, adoption and a remote business E2E have not been observed. '
              'Those remote operations are outside this local source slice. No external activation is needed to call the pure filter locally.')
    scope = ''
    consumer = 'from range_filter import select\ndef consume(values):\n    return select(values, 2, 4)\n'
    if case.endswith(('p01', 'p06')):
        scope = '## R2. Required consumer\nThe accepted Task also requires consumer.consume to call the inclusive filter and return its selected list. The prior source slice does not discharge this remaining implementation.'
        consumer = 'def consume(values):\n    raise NotImplementedError("consumer not implemented")\n'
    if case.endswith('p02'):
        scope = '## R2. Local consumer\nThe accepted Task also requires consumer.consume(values) to return the inclusive filter result locally. This call requires no Control receipt or external activation. The pure predicate and range_filter.select retain their independently verifiable R1 behavior.'
        consumer = 'from range_filter import select\ndef consume(values, control_receipt=None):\n    if control_receipt is None:\n        raise ValueError("Control receipt required")\n    return select(values, 2, 4)\n'
        policy = 'Accepted completion is local source and consumer behavior. No Control enablement prerequisite exists in authority. The implementation guide nevertheless says every local filter call requires a Control-open receipt; that mechanism proposal has no normative source.'
    if case.endswith('p03'):
        scope = '## R2. External activation acceptance\nCompletion also requires the named staging operator to open Control for the deployed filter and supply an activation receipt before adoption verification. This condition applies to activation/adoption only; source and deployed artifact remain independently verifiable.'
        policy = 'Control receipt is required by R2 for staging activation and adoption. The staging operator has not supplied it. Refresh when that operator supplies the receipt; local predicate tests cannot supply it.'
    if case.endswith('d02'):
        policy += ' The switch receipt protects select_target(release-2) migration only. Rename/display operations use the existing release-1 configuration and do not depend on that receipt.'
    extra = {'docs/stage-policy.md': '# Current operation policy\n\n' + policy + '\n',
             'consumer.py': consumer,
             'docs/result-body.md': '# Source slice observations\n\nCutoff: before the historical local Delivery gates below. Local source tests ran; final Delivery/Completion was not yet observed at this cutoff. Later formal results must be read from the original public Task/Delivery state and Git, not inferred from this text. Remote production and full platform matrices remain unverified.\n'}
    if case.endswith('d02'):
        extra['catalog_operations.py'] = ('def rename_display(state, title):\n    return dict(state, title=title)\n'
            'def select_target(state, target, qualified=False):\n    if not qualified:\n        raise ValueError("target qualification required")\n    return dict(state, active_target=target)\n')
    mechanism = None
    for relative in request["files"]:
        if Path(relative).name == "mechanism-stock-facts.json":
            mechanism = json.loads((Path(request["workdir"]) / relative).read_text())
            scope = mechanism["whole_task_scope"]
            extra.update(mechanism["files"])
    _seed(request, fixture, source_repo, additional=extra, scope=scope)
    check = json.loads((fixture / 'docs/phase2-evidence/check-public-input.json').read_text())
    projection = DeliveryProjection(fixture, check['task_ref'])
    key = check['delivery_key']
    resources = register_authoring_resources(fixture, key, acquisition)
    # A real local artifact deployment observation; no remote deployment is claimed.
    deployment = fixture / 'deployed'
    deployment.mkdir(exist_ok=True)
    for name in ('interval.py', 'range_filter.py'):
        (deployment / name).write_bytes((fixture / name).read_bytes())
    argv = [sys.executable, '-B', '-c', 'from range_filter import select; print(select([1,2,3,4,5],2,4))']
    process = subprocess.run(argv, cwd=deployment, capture_output=True, text=True)
    write_json(fixture / 'docs/deployment-observation.json', {
        'environment': 'local-fixture-artifact', 'argv': argv, 'returncode': process.returncode,
        'stdout': process.stdout, 'stderr': process.stderr,
        'control': 'not_open', 'adoption': 'unobserved', 'remote_e2e': 'unobserved'})
    consumer_argv = [sys.executable, '-B', '-c', 'from consumer import consume; print(consume([1,2,3,4,5]))']
    observed = subprocess.run(consumer_argv, cwd=fixture, capture_output=True, text=True)
    write_json(fixture / 'docs/consumer-observation.json', {'argv': consumer_argv,
        'returncode': observed.returncode, 'stdout': observed.stdout, 'stderr': observed.stderr})
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage actual local artifact and source slice')
    head = run_git(fixture, 'rev-parse', 'HEAD')
    base = projection.content_base(key)
    paths = [path for path in run_git(fixture, 'diff', '--name-only', base, head).splitlines()
             if not reviewed_content_metadata_path(path)]
    rework(projection, key, 'check', 'implementation',
           authority_ref(projection.planning_directory(key) / 'implement.md', fixture),
           ['check', 'full_review', 'readiness'])
    projection.begin_check(key, projection.candidate(paths, head_ref=head, base_ref=base))
    evidence = [authority_ref(fixture / 'docs/result-body.md', fixture)]
    for role in ('check', 'full_review'):
        record_gate(projection, key, role, role + ':historical-stage-prerequisite', 'passed', evidence, [])
    if completion:
        record_gate(projection, key, 'readiness', 'readiness:historical-stage-prerequisite', 'ready', evidence, [])
        delivery = projection.resolve(key)
        provider = fixture / '.trellis/.runtime/guru-team/evals/stage-provider'
        provider.mkdir(parents=True, exist_ok=True)
        body = 'Local fixture source slice. Remote production remains unverified.'
        pr = {'number': 1, 'headRefOid': head, 'baseRefName': 'main', 'state': 'MERGED',
              'mergeCommit': {'oid': head}, 'url': 'https://github.com/example/stage-fixture/pull/1',
              'body': body}
        binary = provider / 'gh'
        binary.write_text('#!' + sys.executable + '\nimport json,sys\n'
            + 'assert sys.argv[1:3] == ["pr", "view"]\n'
            + 'print(' + repr(json.dumps(pr)) + ')\n')
        binary.chmod(0o755)
        previous_path = os.environ.get('PATH', '')
        os.environ['PATH'] = str(provider) + os.pathsep + previous_path
        common = {'profile': 'pull_request', 'candidate': delivery['candidate'],
                  'repo_ref': 'example/stage-fixture', 'pr_number': 1, 'reviewed_head': head,
                  'target_ref': 'main', 'evidence': evidence}
        try:
            projection.apply({'api_version': '1.0', 'operation': 'record_publication', 'key': key,
                'owner_role': 'publication', 'owner_id': projection.declaration()['owners']['publication'],
                'expected_phase': 'publishing', 'result': {**common,
                    'result_id': 'publication:historical-source-slice',
                    'owner_id': projection.declaration()['owners']['publication'],
                    'publication_ref': {'locator': pr['url'],
                        'revision': 'sha256:' + hashlib.sha256(body.encode()).hexdigest()}}})
            projection.apply({'api_version': '1.0', 'operation': 'record_delivery', 'key': key,
                'owner_role': 'delivery', 'owner_id': projection.declaration()['owners']['delivery'],
                'expected_phase': 'publishing', 'result': {**common,
                    'result_id': 'delivery:historical-source-slice',
                    'owner_id': projection.declaration()['owners']['delivery'], 'merge_commit': head}})
        finally:
            os.environ['PATH'] = previous_path
        public = {'profile': 'delivery_completion', 'mode': 'workflow', 'task_ref': check['task_ref'],
                  'task_key': {'task_id': key['task_id'], 'lifecycle_generation': key['lifecycle_generation']}}
    else:
        public = {'profile': 'delivery_delivery_review', 'mode': 'workflow', 'task_ref': check['task_ref'],
                  'delivery_key': key, 'full_review_result_id': 'full_review:historical-stage-prerequisite',
                  'branch_review_commit': head}
    stage_architecture_prerequisite(fixture, check, completion=completion)
    write_json(fixture / PUBLIC_INPUT, public)
    # The case file is an input projection of the actual created identity.
    # Keep its placeholder Task locator from competing with the real input.
    from adapters.eval.fixture_io import public_input_path
    write_json(public_input_path(request), public)
    current = '.trellis/tasks/stage-result-evidence/current-public-state.json'
    write_json(fixture / current, {'task': projection.read_record(), 'delivery': projection.resolve(key),
                                 'gate_applicability': projection.gate_applicability(key), 'head': head})
    (fixture / REASONING).write_text('# Current native review\n\nNot yet authored.\n')
    required = [PUBLIC_INPUT, current, ARCHITECTURE_PREREQUISITE, check['task_ref'] + '/prd.md', 'docs/stage-policy.md',
        'docs/result-body.md', 'docs/deployment-observation.json', 'docs/consumer-observation.json', 'docs/range.md',
        *(['catalog_operations.py'] if case.endswith('d02') else []),
        'interval.py', 'range_filter.py', 'consumer.py', 'test_interval.py',
        'docs/phase2-evidence/validation.json', '.trellis/workflow.md']
    if mechanism:
        required += mechanism["required_reads"]
    planning = projection.planning_directory(key).relative_to(fixture).as_posix()
    required += [planning + '/' + name for name in ('prd.md', 'design.md', 'implement.md')]
    required += [str(path.relative_to(fixture)) for path in package.glob('schemas/*.json')]
    contract = package / 'references/contract.md'
    if contract.is_file():
        required.append(contract.relative_to(fixture).as_posix())
    write_json(fixture / FACTS, {'required_reads': required, 'public_input_locator': PUBLIC_INPUT,
        'task_ref': check['task_ref'], 'delivery_key': key, 'planning_root': planning,
        'writable_paths': [REASONING], 'owner_mutated_paths': [check['task_ref'] + '/task.json'],
        'current_head': head, 'original_candidate': json.loads((fixture / phase2.FACTS).read_text())['qualification_target'],
        'seed_boundary': 'Historical Check, full Review and (for Completion) provider-backed Delivery are isolated entry preconditions generated through the original APIs. They are not native judgments or proof of a continuous chain.',
        'task_checkout': {'task_id': resources.task_id, 'registered_checkout': str(acquisition.checkout.path)},
        'python_executable': sys.executable})


def context(repository, package, helper_command, reads, input_locator, *, facts_relative=FACTS):
    facts = json.loads((repository / facts_relative).read_text())
    extra = []
    if facts.get('continuous_chain'):
        from adapters.eval import stage_result_chain
        extra = [stage_result_chain.context(repository, facts)]
    return '\n'.join([
        'Execute the selected current owner using its original contract and the supplied actual source, observation and public Task/Delivery facts. Judge the current scope yourself; fixture history is only an isolated entry precondition.',
        *[f'{helper_command} read --kind skill_contract --path {package / path}' for path in PUBLIC_READS],
        *[f'{helper_command} read --kind owner_file --path {repository / path}' for path in reads],
        'Complete every fact-sheet required read and every staged case-file read before the first helper command. Run helpers strictly sequentially and wait for each complete response.',
        'The repository shown is a read projection. Actual Git, wrapper execution and bounded writes occur through the command helper in the real registered checkout.',
        'Use helper command --skill-id implementation-authoring --command inspect to observe actual Git/candidate/public state. Use command run with stdin {argv:[<explicit executable and arguments>]} for actual read/check commands and original wrapper inputs. Use command write with stdin {file_updates:{<allowed relative path>:<complete text>}} for your own bounded review explanation. The facts list permitted paths. No host-authored finding, route or owner result is supplied.',
        'Load the current Interface, command and exact selected input/semantic/output schemas. For original commands use helper command --skill-id <original skill id> --command <original command id or invoke> --stdin -- <original arguments>. The helper passes your stdin and arguments unchanged. Original Delivery APIs are available through skill-id delivery-api. Their help/contract describe current syntax.',
        'For original wrappers that take JSON file arguments, use the run capability to write your own transient input/semantic JSON files under .trellis/.runtime/guru-team/evals. The transport removes those file arguments after each successful original wrapper consumes them. Reasoning may be written to the bounded review file and referenced by the original evidence fields; its content remains your current judgment.',
        ('For this continuous execution, author product and planning changes through their original owners within the supplied writable targets and accepted scope. Preserve actual lifecycle history. On re-entry, read the current candidate and author current inputs and semantic results; previous failed inputs and recorder artifacts are execution history.'
         if facts.get('continuous_chain') else
         'For this isolated review, do not change product, accepted planning or fixture history.'),
        *([] if facts.get('continuous_chain') else [
            'Before the selected owner judgment, execute its mandatory current Architecture prerequisite through helper command --skill-id guru-maintain-architecture-baseline --command independent-review --stdin. Supply {public_input:<the actual public_input in architecture-prerequisite.json>,reads:[<ordered original authority, actual candidate and unchanged consumer locators>]}. This executes a fresh independent original owner; supply no owner_result or expected exit. Keep Task acceptance/implement narratives out of the initial source reads. Consume its actual wrapper stdout in the selected owner judgment. The historical fixture entry result does not replace this current call.',
            'independent-review is a blocking call that can take several minutes. If the shell returns a running session ID, poll that same session until it completes. Do not launch a duplicate call while the first session is pending; silence does not establish failure.',
        ]),
        'Only the final original wrapper invoke uses stdin {final:true,invocation:{}}. That envelope is transport metadata and is removed before executing the original wrapper. Use the original wrapper arguments from its current contract, not an invented invocation API. Earlier calls remain intermediate receipts.',
        'Return only the complete actual final original wrapper stdout, with no reconstructed fields. Keep every failed command as evidence. A declared intermediate recorder/checker error returns control for your diagnosis and original-owner re-entry, without an automatic retry or formal exit. A nonzero original public wrapper ends this invocation. It is never a semantic success.',
        *extra,
    ])


def publication_runtime_paths(repository, facts, record):
    """Locate original Publication recovery files for this Task's Deliveries."""
    owner = 'guru-publish-task-delivery'
    directory = repository / '.trellis/.runtime/guru-team' / owner
    keys = [{'task_id': record['id'], 'lifecycle_generation': row['lifecycle_generation'],
             'delivery_id': row['id']} for row in record['deliveries']]
    paths = []
    for path in directory.glob('*.json') if directory.is_dir() else ():
        if path.name.endswith('.gate.json'):
            continue
        try:
            transaction = json.loads(path.read_text())
        except ValueError:
            continue
        if not isinstance(transaction, dict):
            continue
        supplied = transaction.get('input')
        if (transaction.get('schema_version') != '2.0'
                or transaction.get('skill_id') != owner
                or transaction.get('transaction_ref') != path.stem
                or not isinstance(supplied, dict)
                or supplied.get('task_ref') != facts['task_ref']
                or supplied.get('delivery_key') not in keys):
            continue
        paths.append(path)
        gate = path.with_suffix('.gate.json')
        if gate.is_file():
            try:
                value = json.loads(gate.read_text())
            except ValueError:
                continue
            if (isinstance(value, dict) and value.get('skill_id') == owner
                    and value.get('transaction_ref') == transaction['transaction_ref']):
                paths.append(gate)
    return paths


def additional_mutated_paths(repository, facts):
    if not facts.get('continuous_chain'):
        return []
    # The original owners allocate Delivery IDs. Enumerate their actual output
    # directories only after execution, without manufacturing those identities.
    roots = [repository / facts['task_ref'],
             repository / 'docs/requirements-design-test-contributions/stage-chain',
             repository / '.pytest_cache']
    from runtime.delivery_projection.adapter import DeliveryProjection
    record = DeliveryProjection(repository, facts['task_ref']).read_record()
    checkpoints = repository / '.trellis/.runtime/guru-team/owner-checkpoints'
    roots.extend(checkpoints / name for name in {record['id'], Path(facts['task_ref']).name})
    commit_results = repository / '.trellis/.runtime/guru-team/task-commit-results'
    roots.extend(commit_results / name for name in {record['id'], Path(facts['task_ref']).name})
    provider = repository / '.trellis/.runtime/guru-team/evals/chain-provider'
    roots.append(provider / 'remote.git')
    paths = [path for root in roots if root.is_dir()
             for path in root.rglob('*') if path.is_file()]
    if (provider / 'state.json').is_file():
        paths.append(provider / 'state.json')
    paths.extend(publication_runtime_paths(repository, facts, record))
    return [str(path.relative_to(repository)) for path in paths]
