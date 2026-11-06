"""Fact-only Planning entry and actual implementation continuation transport.

Initial native cases have no accepted plan or stage result. A later continuation
requires actual predecessor stdout and original Activation for the same fixture.
Historical module preconditions belong to the module tests, not this native seed.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from adapters.eval import phase2_authoring
from adapters.eval.fixture_io import run_git
from adapters.eval.phase2_authoring import write_json

SKILL = 'guru-author-task-plan'
FACTS = '.trellis/tasks/implementation-evidence/public-authoring-facts.json'
RESUME_FACTS = '.trellis/tasks/implementation-evidence/resume-authoring-facts.json'
PUBLIC_INPUT = '.trellis/tasks/implementation-evidence/public-input.json'
OWNER_SCHEMA = 'schemas/semantic-result-2.0.schema.json'
PUBLIC_READS = ('SKILL.md', 'interface.json', 'commands.json')
OWNERS = ('guru-author-task-plan', 'guru-maintain-architecture-baseline',
          'guru-clarify-requirements', 'guru-check-task', 'guru-create-delivery',
          'guru-approve-task-plan', 'guru-activate-delivery',
          'guru-review-contract-wording', 'guru-qualify-root-cause',
          'guru-qualify-normal-scenario', 'guru-qualify-solution-mechanism',
          'guru-maintain-requirements-design-test-ssot')
ENTRY_OWNERS = ('guru-select-workflow-mode', 'guru-sync-base',
                'guru-discover-change-context', 'guru-review-change-request',
                'guru-create-task', 'guru-establish-task-identity',
                'guru-ensure-task-checkout', 'guru-bind-task-session',
                'guru-establish-task-branch-binding')
ENTRY_KIND = 'pre_task_r1'
ENTRY_CONTEXT = 'guru713-r1-entry-v1'
RDT = 'guru-maintain-requirements-design-test-ssot'
RESUME_CASE = 'native-implementation-plan-resume'
RESUME_PROTOCOL_ENV = 'GURU_TEAM_IMPLEMENTATION_RESUME_PROTOCOL'
ACTIVATION_OUTPUT_ENV = 'GURU_TEAM_IMPLEMENTATION_ACTIVATION_OUTPUT'
PLANNING_CONTINUATION_PROTOCOL_ENV = 'GURU_TEAM_IMPLEMENTATION_PLANNING_CONTINUATION_PROTOCOL'
PLANNING_CONTINUATION_FACTS = '.trellis/tasks/implementation-evidence/planning-continuation-facts.json'
CASES = (
    ('native-implementation-plan-premise', 'guru-author-task-plan', 'delivery_initial_review'),
    ('native-implementation-authority-conflict', 'guru-clarify-requirements', 'delivery_active_task_scope_change'),
    ('native-implementation-code-drift', 'guru-check-task', 'delivery_initial_check'),
)
EXECUTION_SURFACE = (
    'A fresh independent reviewer receives only its supplied public input and file reads, not the parent inspect/run stdout. Its first-invocation reads must satisfy the original blind-first contract; Task PRD and implement narratives are excluded from that initial read set.',
    'The inspect command returns the actual complete current diff and identities. The run command can read actual Git before bytes and execute validation. Allowed write targets include diff.patch and validation.json for carrying those raw facts to the separate reviewer; historical observation files remain historical.',
)


def facts_locator(request: dict) -> str:
    if request.get('case_id') == RESUME_CASE:
        return RESUME_FACTS
    return PLANNING_CONTINUATION_FACTS if planning_continuation_requested(request) else FACTS


def initial_request_entry(request: dict) -> bool:
    """Recognize the declared test setup, without selecting a workflow route."""
    if (request.get('case_id') != 'native-implementation-plan-premise'
            or request.get('native_execution_mode') != 'semantic_authoring'
            or planning_continuation_requested(request)):
        return False
    files = request.get('files', [])
    if len(files) != 1 or not request.get('workdir'):
        return False
    source = Path(request['workdir']) / files[0]
    return json.loads(source.read_text()).get('entry_kind') == ENTRY_KIND


def entry_environment(repository: Path) -> dict:
    return {'PATH': str(repository.parent / 'owner-bin') + os.pathsep + os.environ['PATH'],
            'TRELLIS_CONTEXT_ID': ENTRY_CONTEXT, 'PYTHONDONTWRITEBYTECODE': '1',
            'GIT_OPTIONAL_LOCKS': '0'}


def stage_request_entry(request: dict, fixture: Path, source_repo: Path) -> None:
    """Prepare source bytes and clean Git topology, without business identities."""
    from adapters.eval.fixture_io import write_fake_gh
    method_relative = Path('.agents/skills/trellis-brainstorm/SKILL.md')
    method_source = source_repo / method_relative
    if not method_source.is_file():
        raise ValueError('R1 fixture requires the original trellis-brainstorm method '
                         'from the matching installed source at ' + str(method_relative))
    method_target = fixture / method_relative
    method_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(method_source, method_target)
    source = json.loads((Path(request['workdir']) / request['files'][0]).read_text())
    request_body = source['request']['body']
    files = {**source['repository_files'], 'docs/requests/r1.md': request_body,
             'docs/range.md': _implementation_range_authority(request['case_id'])}
    for relative, body in files.items():
        if Path(relative).is_absolute() or '..' in Path(relative).parts:
            raise ValueError('R1 fixture source path must be repository-relative')
        target = fixture / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(body, encoding='utf-8')
    public = {'entry_kind': ENTRY_KIND, 'request_locator': 'docs/requests/r1.md',
              'title': source['request']['title'],
              'boundary': 'Raw standalone R1 request; no Task or semantic predecessor exists.'}
    write_json(fixture / PUBLIC_INPUT, public)
    reads = sorted({*files, PUBLIC_INPUT, '.trellis/workflow.md',
                    '.trellis/spec/workflow/clear-technical-writing.md'})
    write_json(fixture / FACTS, {
        'schema_version': '1.0', 'case_id': request['case_id'], 'entry_kind': ENTRY_KIND,
        'required_reads': reads, 'public_input_locator': PUBLIC_INPUT,
        'candidate_seed': source['candidate_files'],
        'planned_task_id': 'r1-planning-entry', 'context_id': ENTRY_CONTEXT,
        'writable_paths': [FACTS, PUBLIC_INPUT, 'interval.py', 'test_interval.py',
                           'docs/operator-notes.md', 'docs/phase2-evidence/diff.patch',
                           'docs/phase2-evidence/validation.json'],
        'owner_mutated_paths': [], 'python_executable': sys.executable,
        'affected_target_start': {'interval.py': source['repository_files']['interval.py']},
        'seed_boundary': 'Source request and candidate bytes only; every owner result is pending.',
    })
    run_git(fixture, 'add', '.')
    run_git(fixture, 'commit', '-qm', 'stage original R1 request and business baseline')
    head = run_git(fixture, 'rev-parse', 'HEAD')
    run_git(fixture, 'remote', 'add', 'origin', 'https://github.com/example/guru-extension.git')
    run_git(fixture, 'update-ref', 'refs/remotes/origin/main', head)
    primary = fixture.with_name(fixture.name + '-primary')
    fixture.rename(primary)
    run_git(primary, 'worktree', 'add', '-b', 'codex/eval-r1-planning-entry', str(fixture), head)
    remote = fixture.parent / 'source-remote.git'
    run_git(fixture.parent, 'clone', '--bare', '--no-local', str(primary), str(remote))
    write_fake_gh(fixture.parent, 'sync-base', local_remote=remote)


def planning_continuation_requested(request: dict) -> bool:
    return (request.get('case_id') == 'native-implementation-plan-premise'
            and bool(os.environ.get(PLANNING_CONTINUATION_PROTOCOL_ENV)))


def planning_continuation_execution(request: dict) -> tuple[Path, Path, dict]:
    """Expose an actual RDT intermediate result to a fresh same-fixture caller."""
    from adapters.eval.eval_support import package_tree_sha256
    from runtime.delivery_projection.adapter import DeliveryProjection
    from runtime.schema import validate_json
    if not planning_continuation_requested(request):
        raise ValueError('planning continuation requires its explicit private plan-premise entry')
    protocol = json.loads(Path(os.environ[PLANNING_CONTINUATION_PROTOCOL_ENV]).read_text())
    first_request = json.loads(Path(protocol['native_request_path']).read_text())
    if (first_request['case_id'] != 'native-implementation-plan-premise'
            or protocol.get('implementation_facts_locator', FACTS) != FACTS):
        raise ValueError('planning continuation requires the original plan-premise first segment')
    repository = Path(protocol['owner_repository']).resolve()
    facts = json.loads((repository / FACTS).read_text())
    receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
    last = receipts[-1]
    previous = json.loads(last['response']['stdout'])
    envelope = json.loads(last['request'].get('stdin') or '{}')
    if (last['request']['skill_id'] != RDT or last['request']['command'] != 'invoke'
            or last['response']['returncode'] or envelope.get('final') is not True
            or 'invocation' not in envelope
            or previous.get('exit_id') != 'revision_required'
            or previous.get('revision_code') != 'design_revision'
            or previous.get('task_locator') != facts['task_ref']):
        raise ValueError('planning continuation requires actual terminal RDT design_revision stdout')
    package = repository / '.trellis/guru-team/skills/packages' / request['skill_id']
    source_packages = Path(request['package_root']).resolve().parent
    for skill in OWNERS:
        if package_tree_sha256(package.parent / skill) != package_tree_sha256(source_packages / skill):
            raise ValueError('planning continuation source package differs from the first fixture: ' + skill)
    validate_json(previous, package.parent / RDT / 'schemas/public-revision-required-output.schema.json',
                  'preceding_output')
    projection = DeliveryProjection(repository, facts['task_ref'])
    context_id = protocol.get('implementation_context_id') or 'architecture-delivery-eval'
    previous_context = os.environ.get('TRELLIS_CONTEXT_ID')
    os.environ['TRELLIS_CONTEXT_ID'] = context_id
    try:
        current = projection.current(facts['delivery_key'])
    finally:
        if previous_context is None:
            os.environ.pop('TRELLIS_CONTEXT_ID', None)
        else:
            os.environ['TRELLIS_CONTEXT_ID'] = previous_context
    delivery = projection.resolve(facts['delivery_key'])
    if current.get('kind') != 'current' or current.get('key') != facts['delivery_key']:
        raise ValueError('planning continuation requires the same current Task and Delivery')
    locator = '.trellis/tasks/implementation-evidence/planning-continuation-public.json'
    write_json(repository / locator, {'preceding_output': previous, 'current': current, 'delivery': delivery})
    facts['required_reads'] = sorted(set([*facts['required_reads'], facts['public_input_locator'], locator]))
    facts['public_input_locator'] = locator
    facts['current_head'] = run_git(repository, 'rev-parse', 'HEAD')
    facts['current_delivery'] = delivery
    facts['current_selection'] = current
    facts['owner_mutated_paths'] = sorted(set([*facts['owner_mutated_paths'], locator,
                                             PLANNING_CONTINUATION_FACTS]))
    write_json(repository / PLANNING_CONTINUATION_FACTS, facts)
    return package, repository / '.trellis/guru-team/scripts/bash/run-skill-command.sh', {
        'TRELLIS_CONTEXT_ID': context_id,
    }


def resume_execution(request: dict) -> tuple[Path, Path, dict]:
    """Reuse an actual first segment after original Activation, without authoring it."""
    import os
    from adapters.eval.eval_support import package_tree_sha256
    from runtime.delivery_projection.adapter import DeliveryProjection
    if request['case_id'] != RESUME_CASE:
        raise ValueError('implementation resume requires its separately declared test case')
    protocol_path = Path(os.environ[RESUME_PROTOCOL_ENV]).resolve()
    protocol = json.loads(protocol_path.read_text())
    first_request = json.loads(Path(protocol['native_request_path']).read_text())
    if first_request['case_id'] != 'native-implementation-plan-premise':
        raise ValueError('implementation resume requires the plan-premise first segment')
    repository = Path(protocol['owner_repository']).resolve()
    facts = json.loads((repository / FACTS).read_text())
    receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
    last = receipts[-1]
    approved = json.loads(last['response']['stdout'])
    if (last['request']['skill_id'] != 'guru-approve-task-plan'
            or last['request']['command'] not in {'invoke', 'invoke-guru-approve-task-plan'}
            or last['response']['returncode']
            or approved.get('exit_id') != 'approved'
            or approved.get('task_ref') != facts['task_ref']
            or approved.get('delivery_key') != facts['delivery_key']):
        raise ValueError('implementation resume requires actual original Approval stdout')
    package = repository / '.trellis/guru-team/skills/packages' / request['skill_id']
    source_packages = Path(request['package_root']).resolve().parent
    for skill in OWNERS:
        if package_tree_sha256(package.parent / skill) != package_tree_sha256(source_packages / skill):
            raise ValueError('implementation resume source package differs from the first fixture: ' + skill)
    activation = json.loads(Path(os.environ[ACTIVATION_OUTPUT_ENV]).read_text())
    projection = DeliveryProjection(repository, facts['task_ref'])
    current = projection.current(facts['delivery_key'])
    delivery = projection.resolve(facts['delivery_key'])
    from runtime.schema import validate_json
    from adapters.eval.owner_runtime import load_package_runtime_module
    activation_runtime = load_package_runtime_module(
        repository / '.trellis/guru-team/scripts/bash/run-skill-command.sh', 'guru-activate-delivery', 'invoke')
    validate_json(activation, package.parent / 'guru-activate-delivery/schemas/public-delivery-started-output.schema.json', 'activation_output')
    if (activation.get('exit_id') != 'delivery_started'
            or activation.get('task_ref') != facts['task_ref']
            or activation.get('delivery_key') != facts['delivery_key']
            or current.get('kind') != 'current' or current.get('key') != facts['delivery_key']
            or delivery['phase'] != 'implementing'
            or delivery['results']['planning'] is None
            or approved['planning_result_id'] != activation_runtime.planning_identity(
                repository, projection.planning_directory(facts['delivery_key']))
            or projection.gate_applicability(facts['delivery_key'])['planning']['kind'] != 'applicable'
            or activation.get('planning_accepted_result_id') != delivery['results']['planning']['result_id']):
        raise ValueError('implementation resume requires actual matching current Activation')
    # This is the original output and live public state, never a dialogue event.
    locator = 'docs/implementation-continuation-public.json'
    write_json(repository / locator, {'activation_output': activation, 'current': current,
                                      'delivery': delivery})
    facts['required_reads'] = sorted(set([*facts['required_reads'], locator]))
    facts['current_head'] = run_git(repository, 'rev-parse', 'HEAD')
    facts['current_delivery'] = delivery
    facts['current_selection'] = current
    facts['owner_mutated_paths'] = sorted(set([*facts['owner_mutated_paths'], locator, RESUME_FACTS]))
    write_json(repository / RESUME_FACTS, facts)
    return package, repository / '.trellis/guru-team/scripts/bash/run-skill-command.sh', {
        'TRELLIS_CONTEXT_ID': protocol.get('implementation_context_id') or 'architecture-delivery-eval',
    }


class PublicObservationError(ValueError):
    """Carry an original producer failure without changing its response."""

    def __init__(self, process: subprocess.CompletedProcess):
        self.response = {'returncode': process.returncode, 'stdout': process.stdout,
                         'stderr': process.stderr}
        super().__init__('original public observation failed')


def observe_candidate(repository: Path, facts: dict, paths: list[str] | None = None,
                      *, environment: dict | None = None,
                      development_base: str | None = None,
                      observed_target: str | None = None) -> dict:
    """Relay original public facts for the caller's explicitly selected paths."""
    def public(argv):
        result = subprocess.run(argv, cwd=repository, text=True, capture_output=True,
                                check=False, env={**(environment if environment is not None else os.environ),
                                                  'PYTHONDONTWRITEBYTECODE': '1'})
        if result.returncode:
            raise PublicObservationError(result)
        return json.loads(result.stdout)

    current = public([sys.executable, '-B', '.trellis/scripts/delivery.py', 'current', '--json'])
    if current.get('kind') != 'current' or current.get('key') != facts['delivery_key']:
        raise ValueError('original public current does not select this observation Delivery')
    delivery = current['delivery']
    previous = delivery['candidate']
    selected = paths if paths is not None else previous['paths'] if previous else []
    if not selected or not all(isinstance(path, str) and path for path in selected):
        raise ValueError('inspect requires the caller-selected nonempty paths or an existing public candidate')
    head = run_git(repository, 'rev-parse', 'HEAD')
    candidate_argv = ['bash', '.trellis/guru-team/scripts/bash/construct-delivery-candidate.sh',
        '--root', '.', '--task', facts['task_ref'], '--delivery-key', json.dumps(facts['delivery_key']),
        '--head', head, '--paths', *selected]
    for flag, value in (('--development-base', development_base), ('--observed-target', observed_target)):
        if value is not None:
            candidate_argv.extend([flag, value])
    candidate = public(candidate_argv)
    content = public(['bash', '.trellis/guru-team/scripts/bash/run-skill-command.sh',
        '--package-root', '.trellis/guru-team/skills/packages/guru-review-branch',
        '--validator', 'reviewed_content_identity', '--', '--root', '.', '--include-worktree'])['result']
    base = candidate['base_ref']
    from adapters.eval.eval_support import qualification_planning_identity
    qualification_target = {**facts['original_candidate'], 'checkout_head': head,
        'planning_identity': qualification_planning_identity(repository, [
            facts['planning_root'] + '/' + name for name in ('prd.md', 'design.md', 'implement.md')])}
    return {'current_head': head, 'fixed_base': base,
            'status_porcelain': run_git(repository, 'status', '--porcelain=v1'),
            'reviewed_paths': candidate['paths'], 'candidate': candidate,
            'reviewed_content': content,
            'architecture_candidate': {'head': head,
                'content_identity': 'sha256:' + content['sha256']},
            'diff': run_git(repository, 'diff', base), 'current_delivery': delivery,
            'qualification_target': qualification_target,
            'current_selection': current}


def _implementation_range_authority(case_id: str) -> str:
    """Supply complete source definitions, without an owner judgment or result."""
    observation = (
        'The starting snapshot has three test_interval.py methods: '
        'test_lower_and_interior asserts true at 2 and 3 in [2,4]; '
        'test_upper_and_singleton asserts false at (4,2,4) and (2,2,2); '
        'test_outside asserts false at 1 and 5. The supplied candidate design describes '
        'lower <= value < upper. These are observed candidate design/assertion bytes, '
        'distinct from the normative definitions above.\n'
        if case_id == 'native-implementation-plan-premise' else
        'The starting snapshot has four test_interval.py methods: '
        'test_endpoints_and_interior asserts true at 2,3,4 in [2,4]; '
        'test_outside asserts false at 1 and 5; test_singleton asserts true at (2,2,2); '
        'test_negative asserts true at (-2,-4,-2). These are assertion definitions, '
        'not a statement that the implementation passes them.\n'
    )
    return '''# Integer Range

## Authority and navigation

Identity: range-rdt-v1. Status: current authority for the accepted target definitions below.
Source: the standalone inclusive-integer-range request R1. No predecessor definition is replaced.
This authority does not certify that the current implementation satisfies the target.
The public Architecture inheritance is docs/architecture/README.md, range-v1, active.

| Unit | Body | Relationship |
| --- | --- | --- |
| RANGE-REQ-1 | Requirements below | Implemented by RANGE-DES-1; verified by RANGE-TST-1 |
| RANGE-DES-1 | Design below | Owns membership/filter responsibilities for RANGE-REQ-1 |
| RANGE-TST-1 | Verification below | Covers RANGE-REQ-1 through RANGE-DES-1 and the existing caller |

## Requirements: RANGE-REQ-1

contains(value, lower, upper) includes both endpoints, including singleton ranges.
Inputs are integers and lower <= upper. The result is true exactly when lower <= value <= upper;
outside values return false. Negative bounds obey the same comparisons. No I/O or state.
The existing select(values, lower, upper) caller retains every matching list item in input order,
including duplicate matches. Unordered/noninteger inputs have no new policy in this scope.

## Design: RANGE-DES-1

The accepted target assigns mathematical membership to interval.py:contains using integer comparisons.
range_filter.py:select composes contains in its existing list comprehension; it owns selection,
not a separate range policy. Keep both call signatures and the Boolean/list outputs.
Neither module owns I/O, external dependencies, persistence or business rejection.
These are target responsibilities under RANGE-REQ-1 and the public range-v1 Architecture Baseline;
the candidate source and design remain separate evidence of actual implementation.

## Verification: RANGE-TST-1

test_interval.py is the local unittest entry for predicate behavior. The normative strategy covers
lower/interior/upper in [2,4] (2,3,4 true), outside values (1,5 false), singleton (2,2,2 true),
and negative endpoint (-2,-4,-2 true). Review actual assertion content against RANGE-REQ-1.
Run the current Python interpreter with -B -m unittest -v test_interval to obtain actual results.

Direct range_filter.select probes cover the unchanged production consumer: ([1,2,3,4,5],2,4)
returns [2,3,4]; ([1,2,3],2,2) returns [2]; ([4,2,4,1,3],2,4) returns [4,2,4,3].
This verifies endpoint/singleton composition and preserved order/duplicates independently of test helpers.
These are expected target observations, not recorded command results, native review or release proof.

## Starting source observations

The source baseline contains an interval.contains stub raising NotImplementedError and the existing
range_filter.select comprehension. Candidate implementation and assertions are separate actual files.
This source observation establishes no Planning acceptance or implementation result.
''' + observation


def _code_drift_seed_bodies() -> dict[str, str]:
    """Original planning bytes for this private fixture, before acceptance."""
    return {
        'task-prd.md': '''# Inclusive integer range: whole Task requirements

## 1. Sources and terms

The standalone engineering request is R1 below; there is no external Issue.
`docs/range.md`, range-rdt-v1, is the current Requirements/Design/Test authority: RANGE-REQ-1 owns target behavior, RANGE-DES-1 owns predicate/filter responsibilities, and RANGE-TST-1 owns verification relationships. Its starting-source observations are historical facts, not target definitions. `docs/architecture/README.md`, Architecture Baseline, and `docs/architecture/00-foundation/design-constitution.md`, Design Constitution, own Architecture responsibilities. `docs/architecture/06-governance/change-contract.md`, Change Contract, owns review concerns.
Inclusive includes both endpoints; a singleton has lower == upper.

## 2. Background and problem

The supplied interval.contains stub raises NotImplementedError. range_filter.select already composes it to filter values. The missing predicate prevents that caller from returning the documented members.

## 3. Goals and non-goals

Deliver R1 and verify the existing filter caller. Preserve signatures and pure comparison/filter responsibilities. Do not add invalid-input policy, I/O, state, external dependencies, new APIs, migration or deployment work.
Whole Task Completion requires verified R1, applicable quality/Delivery results and a separate whole-scope completion review.

## 4. Callers, scenarios and flow

S1: A caller supplies integers with lower <= upper to contains; observe membership for lower/interior/upper, singleton and negative bounds, and false outside.
S2: select(values, lower, upper) calls contains for each integer list item and retains matching items in input order, including duplicate matches. No external state changes.

## 5. Behavior requirements

R1: contains(value, lower, upper) returns true exactly when lower <= value <= upper for integers with lower <= upper. Both endpoints, singleton ranges and negative endpoints are included. Outside values return false. No I/O or state.
Preserve select's existing signature, predicate composition, order and duplicate matches. No new behavior is specified outside the stated input domain. The selected Delivery design section 3 owns the sole source-design disposition.

## 6. Constraints and dependencies

interval.py owns mathematical membership; range_filter.py composes it without business rejection. Local Python/unittest, source files and current documents are the required inputs. Missing inputs stop dependent work. No external service or predecessor Delivery is required.

## 7. Observable acceptance and validation

AC1 (R1/S1): test_interval.py must accept 2,3,4 in [2,4] and reject 1,5.
AC2 (R1/S1): the same module must accept contains(2,2,2) and contains(-2,-4,-2).
AC3 (R1/S2): direct select probes must return [2,3,4] for ([1,2,3,4,5],2,4), [2] for ([1,2,3],2,2), and [4,2,4,3] for ([4,2,4,1,3],2,4).
These are pending local validations, not production/release proof.

## 8. Actual open questions

No unresolved product or mechanism choice remains. Implementation and validation are pending. New source or responsibility conflicts return to the original requirement or Architecture owner before affected work continues.
''',
        'prd.md': '''# D1: inclusive integer range requirements

## 1. Whole Task sources and terms

Current accepted_scope is `{task_ref}/prd.md`; this Delivery selects its R1 anchor. The actual DeliveryKey/revision are in public Task/Delivery state; selected planning_root is `{planning_ref}`.
Read the whole Task PRD, docs/range.md (range-rdt-v1, RANGE-REQ-1/RANGE-DES-1/RANGE-TST-1), Architecture Baseline, Design Constitution and Change Contract at the canonical paths named there. They own scope, complete R/D/T definitions, Architecture responsibilities and concerns respectively. Inclusive/singleton retain the whole Task meanings.

## 2. Goals and non-goals

D1 covers all R1: replace the missing inclusive predicate and verify the existing filter caller. Preserve signatures and pure responsibilities. No invalid-input policy, I/O, state, dependencies, APIs, migration or deployment is added.

## 3. Starting point, predecessors and remaining responsibility

This is the first Delivery; no predecessor is delivered. Begin from B in design section 1, the unimplemented predicate, existing filter and four existing tests. Local Python/unittest and readable sources are required; missing inputs stop dependent work.
No scope is deferred. Verification and applicable quality/Delivery results are pending. Whole Task Completion still requires its separate whole-scope review.

## 4. Callers, scenarios and flow

D1-S1: contains receives integers with lower <= upper and returns inclusive membership, including singleton and negative endpoints; outside values return false.
D1-S2: select applies contains to each list item and retains matching items in input order with duplicates. No external state transition occurs.

## 5. Complete behavior and constraints

R1: contains(value, lower, upper) returns true exactly when lower <= value <= upper for integers with lower <= upper. Include both endpoints, singleton ranges and negative endpoints. Outside values return false. No I/O or state.
Preserve select(values, lower, upper), its existing composition, order and duplicate matches. No new policy applies outside the stated domain. Membership stays in interval.py; filtering stays in range_filter.py. design section 3 owns the sole source-design disposition.

## 6. Acceptance, validation and open questions

D1-AC1 covers whole Task AC1/AC2 through the four test_interval.py tests: endpoints/interior, outside, singleton and negative bounds.
D1-AC2 covers whole Task AC3 through the three direct select probes and exact results specified there. Design section 8 and implement section 3 provide execution details. Results are pending and establish local behavior only.
No unresolved scope choice remains; a new authority conflict returns to its original owner.

## 7. Canonical references and actual difference

docs/range.md already specifies inclusive endpoints/singletons; the predicate must fulfill it. Architecture Baseline and Design Constitution retain pure predicate/filter ownership; Change Contract retains source/caller review with no project Architecture executable check.
test_interval.py provides the existing assertions; direct select probes cover the unchanged consumer. implement section 6 owns the no-documentation-change decision and reconciliation.
''',
        'design.md': '''# D1: inclusive integer range design

## 1. Goals, requirements and content baseline

Implement R1/D1-S1/S2 and whole Task AC1..AC3. Fixed development baseline B is `{base_ref}`, selected from the observed business baseline HEAD through the original candidate contract. That baseline commit precedes Task/Delivery creation and this planning seed. B already contains the predicate stub, existing filter, four tests and canonical range/Architecture documents. Planning H0 was that observed HEAD; PR target main is separate. Later target observations do not redefine B.
Architecture authority is docs/architecture/README.md (range-v1), docs/architecture/00-foundation/design-constitution.md (range-constitution-v1), and docs/architecture/06-governance/change-contract.md (range-contract-v1/range-concerns-v1). Architecture review checks actual responsibilities, state, dependencies and legal ranges under those contracts.

## 2. Current system, boundary and difference

No predecessor Delivery exists. interval.py raises NotImplementedError. range_filter.py already uses a list comprehension over contains. test_interval.py has four boundary/interior/outside/singleton/negative tests.
Replace the predicate body with inclusive comparisons. Keep the filter, signatures and supported input domain unchanged.

## 3. Source-design disposition (sole location)

| Source promise | Disposition and landing | Reason, impact and upstream handling |
| --- | --- | --- |
| docs/range.md, RANGE-DES-1: membership belongs to contains; select composes it without a separate range policy; preserve signatures, Boolean/list outputs and pure responsibilities | retain; sections 4..8 implement these responsibilities and RANGE-TST-1's predicate/caller verification | Existing target design fits R1; no source design change is needed |
| docs/architecture/README.md, Architecture Baseline: pure predicate in interval.py; production caller in range_filter.py; test_interval.py verifies it; no external dependency, state, deployment or persistence | retain; sections 4..8 preserve these responsibilities and verification | Existing ownership fits R1; no upstream change is needed |
| docs/architecture/00-foundation/design-constitution.md, Design Constitution: mathematical evaluation belongs to the predicate; filter composes it; neither owns I/O/business rejection; current authority defines responsibilities/legal ranges | retain; sections 1/4..6 load current sources and use only comparisons and existing composition | No new authority or rejection is introduced; no upstream disposition is pending |

docs/range.md RANGE-REQ-1's inclusive promise lands in sections 4..6; RANGE-TST-1's verification relationships land in section 8. Its starting-source observations do not certify the current candidate. The Change Contract's actual responsibility/state/dependency/legal-range review includes the unchanged caller.

## 4. Modules, responsibilities and choice

interval.contains receives value/lower/upper and returns lower <= value <= upper. range_filter.select retains its existing predicate-based list comprehension, preserving matching order and duplicates.
test_interval.py calls contains; direct probes call select. Direct integer comparisons suffice for the declared domain; no validation layer or external dependency is required.

## 5. Interfaces and data

Keep contains(value, lower, upper) -> bool and select(values, lower, upper) -> list. Inputs are integers with ordered bounds lower <= upper. True means inclusive membership; false means outside membership.
No new API, field, persistent data or failure status is added. Do not invent unordered/noninteger input policy.

## 6. Order, normal and failure behavior

contains compares both bounds inclusively. select calls it before deciding whether to retain each item. Lower/interior/upper and singleton equality return true; outside values return false. Negative bounds use the same comparisons.
There is no state transition, I/O or new error branch for supported inputs.

## 7. Recovery, compatibility, migration and integration

The unchanged filter consumes the same Boolean interface and preserves ordered duplicate matches. No persistent data or deployment changes, so no migration or release rollback protocol is needed.
Correct local implementation failures and rerun affected validation without relaxing inclusivity or assertions. New source/scope conflicts return to their original owner and refresh affected planning/review before resumption. Preserve unrelated edits.

## 8. Validation design

V1 (R1/S1/AC1..AC2): run Python -B -m unittest -v test_interval. All four tests must pass, including upper, singleton and negative endpoint cases.
V2 (R1/S2/AC3): assert select([1,2,3,4,5],2,4)==[2,3,4], select([1,2,3],2,2)==[2], and select([4,2,4,1,3],2,4)==[4,2,4,3].
V3: inspect the actual B-to-current diff and unchanged caller; check signatures, responsibilities, no I/O/state and assertions against R1.
Results are pending. Local checks do not establish native Agent behavior, installation compatibility or production/release success.

## 9. Canonical references, difference and open questions

docs/range.md already owns inclusive/singleton behavior; interval.py is the implementation difference. Existing test_interval.py and direct V2 probes verify it. The three Architecture documents retain current responsibilities/concerns, with no baseline/ADR contribution planned.
The original RDT writer/reconciliation follows implement section 6. No product/mechanism question blocks this design. New conflicts return to the applicable original owner.
''',
        'implement.md': '''# D1: inclusive integer range implementation and validation

## 1. Inputs and references

Read `{task_ref}/prd.md` R1/scenarios/AC1..AC3, this Delivery PRD sections 4..6, and design sections 1/3..8 for B `{base_ref}`, sole source-design disposition, mechanism, compatibility and validation.
Read docs/range.md (Integer Range) and the canonical Architecture Baseline, Design Constitution and Change Contract for behavior, ownership and review concerns. No predecessor Delivery or external service is required; local Python/unittest and sources are required.

## 2. Ordered steps and file responsibility

I1: Implementation owner reads those inputs and interval.py, range_filter.py and test_interval.py; establish inclusive behavior and caller responsibilities before edits.
I2: After I1, implement lower <= value <= upper in interval.contains. Preserve signatures, purity, filter composition and existing valid assertions.
I3: After I2, execute V1/V2 and inspect V3 below. Correct implementation defects and rerun affected validation.
I4: Before final Phase 2, original RDT/Architecture owners reconcile section 6. Bind the actual candidate to the same B, then obtain applicable original quality/independent review results. No later Delivery owns unfinished R1 work.

## 3. Validation inputs and expected observations

V1: From repository root, use the current Python interpreter with `-B -m unittest -v test_interval`. Expect all four endpoint/interior, outside, singleton and negative tests to pass (R1/AC1..AC2).
V2: From repository root, use the same interpreter with `-B -c "from range_filter import select; assert select([1,2,3,4,5],2,4)==[2,3,4]; assert select([1,2,3],2,2)==[2]; assert select([4,2,4,1,3],2,4)==[4,2,4,3]"` (R1/AC3).
V3: Read complete B-to-current diff, unchanged caller, assertions and canonical sources; verify signatures, comparison ownership, order/duplicates and no I/O/state/dependency changes.
Results remain pending. Command results, semantic Check, native Agent behavior, installation and production/release proof are separate.

## 4. Stop conditions and recovery

Missing sources/Python capability stop dependent work. A failing valid-domain assertion stops completion; repair implementation and rerun without relaxing the assertion.
Requirement/authority conflicts return to the original requirement owner; mechanism/responsibility conflicts return to Author/Architecture. Resume affected work after current planning/review matches the resolution.
Preserve unrelated edits. No persistence/deployment changes, so recovery is a bounded local correction without migration/release rollback protocol. Git/GitHub side effects retain original boundaries.

## 5. Delivery Policy (sole location)

Policy: full. D1 covers all accepted R1 and AC1..AC3, with no deferred scope or later stage.
Independent delivery requires the inclusive predicate, unchanged caller compatibility, actual V1/V2 results, source/diff review and applicable original quality/Delivery outcomes. These are pending.
Delivery merge does not establish whole Task Completion; its original owner separately reviews whole accepted scope and actual results.

## 6. Docs SSOT Plan (sole location)

Strategy: no_docs_update_needed. docs/range.md range-rdt-v1 already defines RANGE-REQ-1's inclusive/ordered integer behavior, RANGE-DES-1's pure predicate/filter responsibilities and RANGE-TST-1's actual predicate/caller verification strategy. Its starting-source observations retain their historical meaning after implementation changes. Architecture Baseline, Design Constitution and Change Contract already describe the unchanged Architecture responsibilities and review concerns.
The implementation fulfills existing behavior; test_interval.py and V2 verify it. No new requirement, responsibility or test policy is introduced.
The original requirements/design/test SSOT writer reviews this no-change decision. Direct consumers are final Phase 2 Docs review and whole Task Completion.
Before final Phase 2, reread actual implementation/caller/assertions and the named canonical documents to reconcile the decision. If a real Docs difference appears, the original writer updates it through its normal path and reconciles before final Check. Do not create an empty contribution, baseline update or ADR solely for this plan.
''',
    }


def stage(request: dict, fixture: Path, package: Path, source_repo: Path) -> None:
    if (request.get('case_id') == 'native-implementation-plan-premise'
            and request.get('native_execution_mode') == 'semantic_authoring'):
        if not initial_request_entry(request):
            raise ValueError('initial R1 native case requires its declared pre_task_r1 source request')
        stage_request_entry(request, fixture.resolve(), source_repo)
        return
    stage_planning_snapshot(request, fixture, package, source_repo)


def stage_planning_snapshot(request: dict, fixture: Path, package: Path, source_repo: Path) -> None:
    """Retain the existing snapshot for module tests and the other native cases."""
    fixture = fixture.resolve()
    from adapters.eval.planning_authoring import acquire_authoring_checkout, register_authoring_resources
    acquisition = acquire_authoring_checkout(fixture, branch_name='eval/implementation')
    case_id = request['case_id']
    plan_conflict = case_id == 'native-implementation-plan-premise'
    authority_conflict = case_id == 'native-implementation-authority-conflict'
    # Reuse environment/business staging with an explicit fact-only boundary.
    # Original owners must produce every subsequent semantic stage result.
    with tempfile.TemporaryDirectory(prefix='implementation-seed-') as temporary:
        workdir = Path(temporary)
        write_json(workdir / 'public.json', {'profile': 'delivery_initial_check', 'mode': 'workflow', 'task_ref': '.trellis/tasks/current'})
        (workdir / 'interval.py').write_text('def contains(value, lower, upper):\n    return lower <= value < upper\n')
        resources = phase2_authoring.stage({**request, 'workdir': temporary,
            'case_id': 'native-owner-common-expectation' if plan_conflict else 'native-owner-finding',
            'files': ['public.json', 'interval.py']}, fixture,
            fixture / '.trellis/guru-team/skills/packages/guru-check-task', source_repo,
            acquisition=acquisition, fact_only=True,
            seed_bodies=_code_drift_seed_bodies() if case_id == 'native-implementation-code-drift' else None,
            range_authority_body=_implementation_range_authority(case_id))
    original_facts = json.loads((fixture / phase2_authoring.FACTS).read_text())
    prior_input = fixture / 'docs/phase2-evidence/check-public-input.json'
    check_input = json.loads(prior_input.read_text()) if prior_input.exists() else original_facts
    from runtime.delivery_projection.adapter import DeliveryProjection
    projection = DeliveryProjection(fixture, check_input['task_ref'])
    key = check_input['delivery_key']
    if resources is None:
        resources = register_authoring_resources(fixture, key, acquisition)
    task_ref = check_input['task_ref']
    planning = projection.planning_directory(key).relative_to(fixture).as_posix()
    projection.select(key)
    new_evidence = 'docs/implementation-observation.md'
    if plan_conflict:
        evidence = ('# RangeFilter consumer specification\n\nRevision: 1. Status: current.\n\n'
                    'select(values, lower, upper) accepts integers with lower <= upper. '
                    'It returns each input value v satisfying lower <= v <= upper, in input order.\n\n'
                    'Examples:\n- select([1, 2, 3, 4, 5], 2, 4) returns [2, 3, 4].\n'
                    '- select([1, 2, 3], 2, 2) returns [2].\n')
    elif authority_conflict:
        evidence = ('# Provider usage policy\n\nRevision: 1. Status: active. Role: normative policy.\n\n'
                    'Application scope: the current contains(value, lower, upper) integer predicate in this repository.\n\n'
                    'For integers with lower <= upper, contains returns true exactly when lower <= value < upper. '
                    'The upper endpoint is excluded. This policy declares no exception.\n')
    else:
        argv = [sys.executable, '-B', '-c',
            'import json; from interval import contains; from range_filter import select; '
            'print(json.dumps({"predicate": [{"input": [v,l,u], "output": contains(v,l,u)} '
            'for v,l,u in [(2,2,4),(3,2,4),(4,2,4),(2,2,2)]], '
            '"selection": {"input": [[1,2,3,4,5],2,4], "output": select([1,2,3,4,5],2,4)}}))']
        observed = subprocess.run(argv, cwd=fixture, capture_output=True, text=True, check=False)
        receipt = {'argv': argv, 'returncode': observed.returncode,
                   'stdout': observed.stdout, 'stderr': observed.stderr}
        evidence = '# Local process observation\n\nSource: execution against the supplied checkout.\n\n```json\n' + json.dumps(receipt, indent=2) + '\n```\n'
    (fixture / new_evidence).write_text(evidence)
    independent = fixture / 'docs/operator-notes.md'
    independent.write_text('# Operator notes\n\nRange predicates have no I/O.\n')
    # Stage newly available evidence and the independent target as starting
    # facts; no candidate edit or new semantic result is written here.
    run_git(fixture, 'add', new_evidence, 'docs/operator-notes.md')
    run_git(fixture, 'commit', '-qm', 'stage newly available implementation evidence')
    public = {'task_ref': task_ref, 'delivery_key': key, 'planning_root': planning,
              'current': projection.current(key), 'source_evidence': new_evidence,
              'boundary': 'Entry facts, not an original Skill invocation input.'}
    write_json(fixture / PUBLIC_INPUT, public)
    reads = ['.trellis/workflow.md', task_ref + '/prd.md', *[planning + '/' + name for name in ('prd.md', 'design.md', 'implement.md')],
             'docs/range.md', new_evidence, 'interval.py', 'range_filter.py', 'test_interval.py',
             'docs/operator-notes.md', 'docs/phase2-evidence/validation.json',
             'docs/architecture/README.md', 'docs/architecture/00-foundation/design-constitution.md',
             'docs/architecture/06-governance/change-contract.md']
    from adapters.eval.owner_runtime import load_package_runtime_module
    approval = load_package_runtime_module(
        fixture / '.trellis/guru-team/scripts/bash/run-skill-command.sh',
        'guru-approve-task-plan', 'common')
    approval_checkpoint = approval.checkpoint(
        fixture, fixture / task_ref, 'planning-approval.json', key).relative_to(fixture).as_posix()
    write_json(fixture / FACTS, {'schema_version': '1.0',
        # Initial reads bind the supplied business facts. Each selected owner
        # loads its public contracts at its original workflow step.
        'required_reads': reads, 'public_input_locator': PUBLIC_INPUT,
        'task_ref': task_ref, 'delivery_key': key, 'planning_root': planning,
        'case_id': case_id,
        'seed_boundary': 'Actual current Planning and unaccepted candidates. No current semantic stage result is supplied.',
        'writable_paths': [task_ref + '/prd.md', *[planning + '/' + name for name in (
            'prd.md', 'design.md', 'implement.md', 'implement.jsonl', 'check.jsonl')],
            'interval.py', 'test_interval.py', 'docs/operator-notes.md',
            'docs/phase2-evidence/diff.patch', 'docs/phase2-evidence/validation.json'],
        'owner_mutated_paths': [*phase2_authoring.owner_mutated_paths(fixture), approval_checkpoint],
        'current_head': run_git(fixture, 'rev-parse', 'HEAD'),
        'original_candidate': original_facts['qualification_target'],
        'declaration': projection.declaration(),
        'current_delivery': projection.resolve(key),
        'current_selection': projection.current(key),
        'python_executable': sys.executable,
        'task_checkout': {'task_id':resources.task_id,
            'lifecycle_generation':resources.lifecycle_generation,'branch_name':resources.branch_name,
            'binding_revision':resources.binding_revision,'registered_checkout':str(acquisition.checkout.path),
            'topology':acquisition.checkout.topology},
        'affected_target_start': {'interval.py': (fixture / 'interval.py').read_text()},
    })


def context(repository: Path, package: Path, helper_command: str, reads: list[str], input_locator: Path, *, facts_relative: str = FACTS) -> str:
    facts = json.loads((repository / facts_relative).read_text())
    planning_segment = (facts.get('case_id') == 'native-implementation-plan-premise'
                        and facts_relative != RESUME_FACTS)
    request_entry = facts.get('entry_kind') == ENTRY_KIND and 'delivery_key' not in facts
    return '\n'.join([
        ('Start from the supplied original standalone R1 request and clean repository. No Task, accepted scope, Delivery or semantic predecessor exists. The installed workflow owns the actual Intake and Planning sequence.'
         if request_entry else
         'Continue from the actual preceding owner output and matching public state. Author each next input from its original contract and actual predecessor output.'
         if facts_relative in (PLANNING_CONTINUATION_FACTS, RESUME_FACTS) else
         'Start from the actual current Planning and supplied unaccepted candidate files. No Planning acceptance, Activation or Check result is supplied.'),
        *([
            'Remain the workflow caller for this entire requested Planning segment. A selected Skill returns one typed exit to you; that return completes only the inner Skill invocation.',
            'Consume each actual public output through its unique consumer in the current installed workflow, within this segment. Read that consumer\'s original contract and assemble its input from the actual predecessor output. A successful inner invocation alone is not an applicable earlier stop.',
            'Before marking an invocation final, judge whether the actual Planning Approval or an applicable original stop has been reached. Otherwise continue the original workflow. The transport does not make this judgment or choose the next owner.',
        ] if request_entry else []),
        f'Repository evidence projection (file reads only): {repository}',
        'This projection has no Git metadata. Forwarded commands execute in the separate original owner checkout. Resolve command paths relative to that checkout: use . when an original --root argument is required. Keep Task and planning locators repository-relative; do not use an absolute evidence-projection path as the execution root.',
        f'Fact sheet: {repository / facts_relative}',
        *[f'{helper_command} read --kind owner_file --path {repository / path}' for path in reads],
        f'{helper_command} read --kind owner_file --path {input_locator}',
        'The entry file contains current identity and business evidence, not a ready-made Skill input. Read the public current state and installed workflow, then select the applicable original owner yourself.',
        'Read the fact sheet and its required source, candidate, caller and assertion files before the first helper command. Load each selected original Skill, Interface and its necessary references, schemas and examples to assemble its invocation. All production calling knowledge must come from those public contracts.',
        'Use the private transport as command --skill-id <original skill-id> --command <original command-id or invoke> --stdin -- <original arguments>. Stdin is passed unchanged. The delivery-api transport executes the original installed delivery.py with the selected subcommand and arguments. Commands run in the owner checkout. The helper supplies no intermediate DTO, semantic result or route.',
        '--stdin reads actual process input; defining a payload variable does not send it. Use a pipe or a quoted heredoc in a non-interactive shell. This example supplies only transport syntax; choose the command, arguments and JSON from the original public contract:',
        '```bash\n'
        f"{helper_command} command --skill-id <skill> --command <command> --stdin -- <original arguments> <<'GURU_COMMAND_JSON'\n"
        '<current-command-input-json>\n'
        'GURU_COMMAND_JSON\n```',
        'Use implementation-authoring write with {file_updates:{relative_path:complete_text}} to transport bounded file bytes. Use implementation-authoring run with {argv:[executable,arguments...]} to execute a process and return its actual stdout, stderr and exit. These operations make no semantic judgment.',
        'Use implementation-authoring inspect with {paths:[caller-selected content paths]} to obtain the original public candidate and content-identity producer results. Optional development_base and observed_target fields pass unchanged to the original --development-base and --observed-target flags. Empty stdin only reuses an existing public candidate path list. Choose production arguments from the original public contracts.',
        *([
            'This is an independent evaluation sample, not a continuation of an older current/g0 fixture or the source repository Task. Keep the supplied planned Task name within this test repository; choose the actual current-date TaskRef through the original Creation contract.',
            'After an actual Task or Delivery created stdout, implementation-authoring observe-entry accepts {producer_skill:<that original owner>,producer_stdout:<complete actual stdout string>}. It checks that command receipt and rereads public current, exposing only observed identities and exact file targets. It supplies no source selection or stage result.',
            'After actual scope acceptance and explicit Delivery Creation, implementation-authoring stage-candidate accepts empty JSON. It writes the supplied half-open candidate bytes into the actual current planning directory and executes raw validation. It leaves root requirements, accepted scope and gates to their original owners. This operation is test setup, not an Author result.',
            'The initial required reads remain the supplied source reads. Read newly produced Task/planning documents through implementation-authoring run using the original checkout and consume its full stdout. Public predecessor outputs remain call-local; never reconstruct source_selection from these observation facts.',
        ] if request_entry else []),
        'Run helper commands sequentially and consume their complete actual responses. For the final original wrapper only, wrap its stdin in eval-only {final:true,invocation:<actual original stdin>}; the helper removes these transport fields. Preserve the original argv and envelope form read from that owner.',
        'If a command tool returns a running session, retain its session ID and collect completion, exit, stdout and stderr before starting another helper. Capture complete helper output before displaying it; a truncated display cannot supply a missing DTO. Starting the same helper again does not wait for its first process.',
        'Capturing a read response in a file does not put its body in your model-visible context. For each full-body read required by the original public contract, display the complete captured body in consecutive bounded chunks before using it to assemble or invoke that owner. Byte counts, hashes, searches and summaries do not replace the body. If a tool display is truncated, display the missing ranges before continuing. Keep the original read order.',
        'For an independent Architecture assessment, the private independent-review transport accepts {public_input:<your original input>,reads:[ordered relative locators]}. It launches the original fresh worker and returns its actual original wrapper stdout. Supply no reviewer owner_result, finding or exit; follow the original independence/read contract.',
        'Begin reads with Constitution, Baseline and project change contract. Repeated entries from the reviewer method\'s exact automatically required public-contract set retain their method coverage role and may already have been read. Actual candidate and consumer evidence must follow those authorities. If a contract itself changes, its method preload alone does not review that change: supply the actual design, full diff or source evidence after authority.',
        *EXECUTION_SURFACE,
        'Every stage must consume real predecessor outputs. No metadata, historical fixture narrative, earlier command success or transport receipt establishes semantic approval. Early legitimate stops remain real stops and do not prove the later implementation or Check scenario.',
        ('This first segment ends at actual Planning Approval or an earlier applicable original stop. Original plan presentation/acceptance and Activation occur outside this segment. Only a later same-fixture continuation with actual Activation stdout may claim after-acceptance implementation evidence.'
         if planning_segment else
         'Continue the applicable original workflow from the actual current stage. Produce the necessary original prerequisites before implementation or Check; if a real prerequisite or authority remains missing, preserve that stop. Claim after-acceptance behavior only when its actual predecessor and Activation outputs exist.'),
        'Return only the final original semantic owner wrapper stdout. Preserve all original failures. Ordinary command errors leave the transport available for your own diagnosis, correction or stop through the original public help/contracts. The host never retries, corrects arguments or chooses a continuation. Only an explicitly final successful original semantic wrapper ends this invocation.',
        *([
            'After judging that this segment has reached its actual endpoint, capture the final original invoke stdout separately and keep its complete value in call-local memory. Intermediate public exits and recorder/checker receipts still belong to their original consumers.',
            'Printing stdout in a tool does not deliver your final message. Parse that final original stdout with json.loads, then render the complete object with json.dumps(..., ensure_ascii=False, indent=2) for your final reply.',
            'Verify that your final reply is the same complete JSON object, preserving its fields and their order with only JSON whitespace changes. Do not manually assemble braces, reconstruct fields, trim invalid trailing characters, or recover output from trace receipts. Invalid JSON remains an original error to handle truthfully.',
        ] if request_entry else []),
    ])


class ImplementationCommands:
    """Private command transport; the native owner selects every continuation."""

    owners = OWNERS

    def __init__(self, repository: Path, environment: dict, receipts_path: Path, *, facts_relative: str = FACTS):
        self.repository = repository
        self.environment = environment
        self.receipts_path = receipts_path
        self.facts_relative = facts_relative
        if json.loads((repository / facts_relative).read_text()).get('entry_kind') == ENTRY_KIND:
            self.owners = (*OWNERS, *ENTRY_OWNERS)
        self.receipts = []
        self.terminal = False
        self.independent_reviewer = None

    def public_query(self, script: str, *arguments: str) -> dict:
        process = subprocess.run([sys.executable, '-B', '.trellis/scripts/' + script,
                                  *arguments, '--json'], cwd=self.repository,
                                 env=self.environment, text=True, capture_output=True, check=False)
        if process.returncode:
            raise PublicObservationError(process)
        return json.loads(process.stdout)

    def observe_entry(self, value: dict) -> dict:
        """Observe a completed public creation; never create or select an object."""
        skill = value['producer_skill']
        if skill not in {'guru-create-task', 'guru-create-delivery'}:
            raise ValueError('observe-entry requires an original Task or Delivery creator')
        previous = next((row for row in reversed(self.receipts)
                         if row['request']['skill_id'] == skill
                         and row['request']['command'] in {'invoke', 'invoke-' + skill}
                         and row['response']['returncode'] == 0), None)
        if previous is None:
            raise ValueError('observe-entry requires the complete actual creator stdout')
        output = json.loads(value['producer_stdout'])
        if output != json.loads(previous['response']['stdout']):
            raise ValueError('observe-entry requires the complete actual creator stdout')
        if output.get('exit_id') != 'created':
            raise ValueError('observe-entry requires an actual created exit')
        facts = json.loads((self.repository / self.facts_relative).read_text())
        if facts.get('entry_kind') != ENTRY_KIND:
            raise ValueError('observe-entry belongs to the R1 request fixture')
        task = self.public_query('task.py', 'current')['current_task']
        if task is None or task['dir'] != output['task_ref']:
            raise ValueError('public current does not match the actual created Task')
        if skill == 'guru-create-task' and (task['id'], task['lifecycle_generation']) != (
                output['task_id'], output['lifecycle_generation']):
            raise ValueError('public current has a different created Task generation')
        task_ref = task['dir']
        if facts.get('task_ref', task_ref) != task_ref:
            raise ValueError('R1 observation cannot switch an already observed Task')
        facts['task_ref'] = task_ref
        facts['current_head'] = run_git(self.repository, 'rev-parse', 'HEAD')
        facts['owner_mutated_paths'] = sorted(set([
            *facts['owner_mutated_paths'], task_ref + '/task.json']))
        facts['writable_paths'] = sorted(set([*facts['writable_paths'], task_ref + '/prd.md']))
        if skill == 'guru-create-delivery':
            current = self.public_query('delivery.py', 'current')
            if current.get('kind') != 'current' or current.get('key') != output['delivery_key']:
                raise ValueError('public current does not match the actual created Delivery')
            delivery = current['delivery']
            if delivery['planning_root'] != output['planning_root']:
                raise ValueError('public planning_root differs from actual creator stdout')
            if facts.get('delivery_key', current['key']) != current['key']:
                raise ValueError('R1 observation cannot switch an already observed Delivery')
            planning = (Path(task_ref) / delivery['planning_root']).as_posix()
            facts.update(delivery_key=current['key'], planning_root=planning,
                         current_delivery=delivery, current_selection=current,
                         original_candidate={'repo_locator': '.', 'task_ref': task_ref,
                                             'diff_locator': 'docs/phase2-evidence/diff.patch'})
            facts['writable_paths'] = sorted(set([*facts['writable_paths'], *[
                planning + '/' + name for name in (
                    'prd.md', 'design.md', 'implement.md', 'implement.jsonl', 'check.jsonl')]]))
            from adapters.eval.owner_runtime import load_package_runtime_module
            approval = load_package_runtime_module(
                self.repository / '.trellis/guru-team/scripts/bash/run-skill-command.sh',
                'guru-approve-task-plan', 'common')
            checkpoint = approval.checkpoint(self.repository, self.repository / task_ref,
                                             'planning-approval.json', current['key'])
            facts['owner_mutated_paths'].append(checkpoint.relative_to(self.repository).as_posix())
        write_json(self.repository / self.facts_relative, facts)
        write_json(self.repository / PUBLIC_INPUT, {
            'entry_kind': ENTRY_KIND, 'task_ref': task_ref,
            **({'current': facts['current_selection']} if 'current_selection' in facts else {}),
            'boundary': 'Observed public identity only; no semantic predecessor is stored.'})
        return {'task_ref': task_ref, **({'delivery_key': facts['delivery_key'],
                                        'planning_root': facts['planning_root']}
                                       if 'delivery_key' in facts else {})}

    def stage_entry_candidate(self) -> dict:
        """Copy the raw candidate only after the original owners establish its target."""
        facts = json.loads((self.repository / self.facts_relative).read_text())
        if facts.get('entry_kind') != ENTRY_KIND or 'delivery_key' not in facts:
            raise ValueError('stage-candidate requires the observed R1 Delivery')
        current = self.public_query('delivery.py', 'current')
        if current.get('kind') != 'current' or current['key'] != facts['delivery_key']:
            raise ValueError('stage-candidate requires the same public current Delivery')
        delivery = current['delivery']
        if delivery['phase'] != 'planning' or any(delivery['results'].values()):
            raise ValueError('stage-candidate cannot overwrite an accepted or progressed plan')
        task = self.public_query('task.py', 'current')['current_task']
        if (task is None or task['dir'] != facts['task_ref']
                or task['accepted_scope'] is None
                or task['accepted_scope'] != delivery['scope_ref']['authority']):
            raise ValueError('stage-candidate requires the same publicly accepted Task scope')
        if any(row['request']['skill_id'] == 'implementation-authoring'
               and row['request']['command'] == 'stage-candidate'
               and row['response']['returncode'] == 0 for row in self.receipts):
            raise ValueError('the R1 candidate seed was already written')
        planning = Path(facts['task_ref']) / delivery['planning_root']
        seed = facts['candidate_seed']
        targets = {'interval.py': seed['interval.py'], **{
            (planning / name).as_posix(): seed[name] for name in (
                'prd.md', 'design.md', 'implement.md', 'implement.jsonl', 'check.jsonl')}}
        if not set(targets).issubset(facts['writable_paths']):
            raise ValueError('candidate targets differ from the observed public planning directory')
        for relative, body in targets.items():
            target = self.repository / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(body, encoding='utf-8')
        argv = [sys.executable, '-B', '-m', 'unittest', '-v', 'test_interval']
        process = subprocess.run(argv, cwd=self.repository, env=self.environment,
                                 capture_output=True, text=True, check=False)
        validation = {'argv': argv, 'returncode': process.returncode,
                      'stdout': process.stdout, 'stderr': process.stderr}
        write_json(self.repository / 'docs/phase2-evidence/validation.json', validation)
        diff = self.repository / 'docs/phase2-evidence/diff.patch'
        diff.write_text(run_git(self.repository, 'diff', 'HEAD') + '\n')
        facts['affected_target_start'] = {'interval.py': seed['interval.py']}
        facts.pop('candidate_seed')
        write_json(self.repository / self.facts_relative, facts)
        return {'written_paths': [*targets, 'docs/phase2-evidence/validation.json',
                                  'docs/phase2-evidence/diff.patch'], 'validation': validation}

    def record_response(self, payload: dict, result: dict) -> None:
        facts = json.loads((self.repository / self.facts_relative).read_text())
        states = {relative: hashlib.sha256((self.repository / relative).read_bytes()).hexdigest()
                  for relative in facts['writable_paths'] if (self.repository / relative).is_file()}
        self.receipts.append({'request': payload, 'response': result, 'target_states_after': states})
        write_json(self.receipts_path, self.receipts)

    def forward(self, payload: dict) -> dict:
        skill, command = payload['skill_id'], payload['command']
        arguments = list(payload['arguments'])
        stdin = payload.get('stdin', '')
        if self.terminal:
            raise ValueError('implementation command follows the terminal original wrapper')
        final = False
        if stdin and not (skill == 'implementation-authoring' and command == 'run'):
            try:
                value = json.loads(stdin)
            except json.JSONDecodeError:
                # Ordinary owner input remains opaque here. Its original
                # wrapper owns malformed-input diagnostics.
                value = None
            if isinstance(value, dict) and 'final' in value and 'invocation' in value:
                final = value['final'] is True
                stdin = json.dumps(value['invocation'], ensure_ascii=False)
        if final and skill in ('delivery-api', 'implementation-authoring'):
            raise ValueError('only an original semantic public wrapper can terminate implementation evidence')
        if skill == 'implementation-authoring' and command in {'observe-entry', 'stage-candidate'}:
            try:
                output = (self.observe_entry(json.loads(stdin)) if command == 'observe-entry'
                          else self.stage_entry_candidate())
                result = {'returncode': 0, 'stdout': json.dumps(output) + '\n', 'stderr': ''}
            except PublicObservationError as error:
                result = error.response
            self.record_response(payload, result)
            return result
        if skill == 'guru-maintain-architecture-baseline':
            if command != 'independent-review' or self.independent_reviewer is None:
                raise ValueError('Architecture assessment requires its actual fresh independent worker')
            result = self.independent_reviewer(json.loads(stdin))
            self.record_response(payload, result)
            if final and result['returncode'] == 0:
                self.terminal = True
            return result
        if skill == 'implementation-authoring' and command == 'inspect':
            facts = json.loads((self.repository / self.facts_relative).read_text())
            options = json.loads(stdin) if stdin else {}
            try:
                result = {'returncode': 0, 'stdout': json.dumps(observe_candidate(
                    self.repository, facts, options.get('paths'), environment=self.environment,
                    development_base=options.get('development_base'),
                    observed_target=options.get('observed_target'))) + '\n', 'stderr': ''}
            except PublicObservationError as error:
                result = error.response
            self.record_response(payload, result)
            return result
        if skill == 'implementation-authoring' and command == 'run':
            try:
                argv = json.loads(stdin)['argv']
                if not isinstance(argv, list) or not argv or not all(isinstance(part, str) for part in argv):
                    raise ValueError('run requires a nonempty argv array of strings')
            except (ValueError, KeyError, TypeError) as error:
                result = {'returncode': 0, 'stdout': json.dumps({'request_error': str(error),
                    'returncode': 2, 'stdout': '', 'stderr': 'Supply run stdin as JSON {"argv":[...]}.'}) + '\n', 'stderr': ''}
                self.record_response(payload, result)
                return result
            try:
                process = subprocess.run(argv, cwd=self.repository, env=self.environment,
                    text=True, capture_output=True, check=False)
            except OSError as error:
                process = subprocess.CompletedProcess(argv, 127, '', str(error))
            result = {'returncode': 0, 'stdout': json.dumps({'argv': argv,
                'returncode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr}) + '\n', 'stderr': ''}
            self.record_response(payload, result)
            return result
        if skill == 'implementation-authoring' and command == 'write':
            value = json.loads(stdin)
            facts = json.loads((self.repository / self.facts_relative).read_text())
            updates = value['file_updates']
            for relative, content in updates.items():
                if relative not in facts['writable_paths']:
                    raise ValueError('implementation authoring write is outside the supplied targets')
                (self.repository / relative).write_text(content)
            result = {'returncode': 0, 'stdout': json.dumps({'written_paths': list(updates)}) + '\n', 'stderr': ''}
            self.record_response(payload, result)
            return result
        if skill == 'delivery-api':
            argv = [sys.executable, '-B', str(self.repository / '.trellis/scripts/delivery.py'), command, *arguments]
        else:
            if skill not in self.owners:
                raise ValueError('implementation command has no supplied existing owner')
            owner = self.repository / '.trellis/guru-team/skills/packages' / skill
            interface = json.loads((owner / 'interface.json').read_text())
            command_id = interface['public_contracts']['invocation']['command_id'] if command == 'invoke' else command
            # Some Interfaces name the shared dispatcher. The selected public
            # wrapper still declares one concrete command in its launcher.
            if command_id == 'run-skill-command':
                command_id = 'invoke-' + skill
            commands = json.loads((owner / 'commands.json').read_text())['commands']
            declared = next((row for row in commands if row['id'] == command_id), None)
            if declared is None:
                raise ValueError('implementation command is not declared by its original owner')
            if final and command_id not in (
                    interface['public_contracts']['invocation']['command_id'], 'invoke-' + skill):
                raise ValueError('only an original semantic public wrapper can terminate implementation evidence')
            if command == 'invoke':
                relative = interface['public_contracts']['invocation']['wrapper']
            else:
                relative = next(row['command'] for row in interface['validators']
                                if row['runtime_command'] == command_id)
            argv = [str(owner / relative), *arguments]
        process = subprocess.run(argv, cwd=self.repository, env=self.environment,
            input=stdin, capture_output=True, text=True, check=False)
        result = {'returncode': process.returncode, 'stdout': process.stdout, 'stderr': process.stderr}
        if final and process.returncode == 0 and skill == 'guru-check-task' and command == 'invoke':
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument('--input')
            parser.add_argument('--invocation')
            selected, _ = parser.parse_known_args(arguments)
            if selected.input and not selected.invocation:
                supplied = Path(selected.input)
                if not supplied.is_absolute():
                    supplied = self.repository / supplied
                temporary = self.repository / '.trellis/.runtime/guru-team/evals/phase2-public-input.json'
                if supplied.resolve() == temporary.resolve():
                    temporary.unlink(missing_ok=True)
        self.record_response(payload, result)
        if final and process.returncode == 0:
            try:
                output = json.loads(process.stdout)
            except (ValueError, TypeError):
                output = None
            if isinstance(output, dict) and output.get('exit_id') in {
                    row['exit_id'] for row in interface['public_contracts']['outputs']}:
                self.terminal = True
        return result


def public_reads(package: Path) -> tuple[str, ...]:
    identity = json.loads((package / 'interface.json').read_text())['id']
    reference = 'references/authoring.md' if identity == 'guru-author-task-plan' else 'references/contract.md'
    return (*PUBLIC_READS, reference)


def validate_trace(payload: dict, protocol: dict, public_stdout: str) -> list[str]:
    """Bind actual command/read records; semantic continuation remains AI-owned."""
    from adapters.eval.eval_constants import stdout_digest
    receipts = json.loads(Path(protocol['implementation_receipts_path']).read_text())
    commands = [event for event in payload['events'] if event['kind'] == 'command']
    if len(commands) != len(receipts) or not commands or payload['events'][-1] != commands[-1]:
        raise ValueError('implementation trace is missing actual commands or terminal wrapper')
    repository = Path(protocol['repository_projection_root'])
    facts_relative = protocol.get('implementation_facts_locator', FACTS)
    facts = json.loads((repository / facts_relative).read_text())
    required = {str(repository / facts_relative), *(str(repository / relative) for relative in facts['required_reads'])}
    writable_states = {str(repository / relative): protocol.get('writable_preimages', {}).get(str(repository / relative))
                       for relative in facts['writable_paths']}
    reads = set()
    index = 0
    for event in payload['events']:
        if event.get('request_sha256') != payload['request_sha256']:
            raise ValueError('implementation trace event has a different request identity')
        if event['kind'] == 'read':
            path = Path(event['path'])
            observed = (writable_states[str(path)] if str(path) in writable_states else
                        hashlib.sha256(path.read_bytes()).hexdigest())
            if event['sha256'] != observed:
                raise ValueError('implementation read differs from its state at that trace position')
            reads.add(event['path'])
            continue
        if event['kind'] != 'command':
            raise ValueError('implementation trace contains a non-command transport event')
        receipt = receipts[index]
        index += 1
        request, response = receipt['request'], receipt['response']
        expected = {'kind': 'command', 'skill_id': request['skill_id'], 'command': request['command'],
            'arguments': request['arguments'],
            'stdin_sha256': hashlib.sha256(request['stdin'].encode()).hexdigest(),
            'returncode': response['returncode'], 'stdout_sha256': stdout_digest(response['stdout']),
            'stderr_sha256': hashlib.sha256(response['stderr'].encode()).hexdigest(),
            'request_sha256': payload['request_sha256']}
        if event != expected:
            raise ValueError('implementation trace differs from the actual original command receipt')
        if not required.issubset(reads):
            raise ValueError('implementation command preceded the supplied source and candidate reads')
        writable_states = {str(repository / relative): receipt['target_states_after'].get(relative)
                           for relative in facts['writable_paths']}
    last = receipts[-1]
    try:
        final = json.loads(last['request']['stdin'])
    except json.JSONDecodeError as error:
        raise ValueError('implementation terminal stdout is not the final original wrapper result: '
                         'missing explicit final marker') from error
    if (not isinstance(final, dict)
            or last['request']['command'] not in {'invoke', 'independent-review', 'invoke-' + last['request']['skill_id']} or final.get('final') is not True
            or 'invocation' not in final or last['response']['returncode'] != 0
            or stdout_digest(last['response']['stdout']) != stdout_digest(public_stdout)):
        raise ValueError('implementation terminal stdout is not the final original wrapper result')
    if payload.get('terminal_skill_id') != last['request']['skill_id']:
        raise ValueError('implementation terminal producer identity differs from its actual wrapper')
    package = repository / '.trellis/guru-team/skills/packages' / last['request']['skill_id']
    interface = json.loads((package / 'interface.json').read_text())
    output = json.loads(public_stdout)
    exits = {row['id'] for row in interface['external_exits']}
    if output.get('exit_id') not in exits:
        raise ValueError('implementation terminal output is not an original owner exit')
    return ['public_invocation', 'evals_not_loaded', 'private_runtime_not_read']
