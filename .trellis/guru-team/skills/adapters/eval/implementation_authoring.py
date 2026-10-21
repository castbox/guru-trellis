"""Existing implementation-owner continuation facts and private native transport.

The fixture supplies a previously accepted plan as a starting fact. Only a
native owner can judge new evidence, choose a continuation, or restore work.
"""
from __future__ import annotations

import argparse
import json
import hashlib
import os
from pathlib import Path
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
    'The original record-phase2-check --input argument accepts a JSON file locator, or - with the JSON in stdin; it does not accept inline JSON as that argument. For an invocation using --input FILE, the named file supplies the public input, not JSON sent separately through stdin. Read the current command contract and prepare the actual input for the selected call.',
    'If the complete diff includes Task PRD, implement or acceptance narratives, prepare readable original authority, candidate/source and consumer material yourself under the original blind-first contract. Keep those narratives out of the initial input, including narrative patch hunks. Preserve the complete candidate for the original owner\'s review; input isolation does not narrow its scope.',
)


def facts_locator(request: dict) -> str:
    if request.get('case_id') == RESUME_CASE:
        return RESUME_FACTS
    return PLANNING_CONTINUATION_FACTS if planning_continuation_requested(request) else FACTS


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
            or last['request']['command'] != 'invoke' or last['response']['returncode']
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


def observe_candidate(repository: Path, facts: dict) -> dict:
    """Read actual complete content facts after owner writes; choose no route."""
    from adapters.eval.owner_runtime import load_package_runtime_module
    from runtime.delivery_projection.adapter import DeliveryProjection
    from runtime.reviewed_content import reviewed_content_identity, reviewed_content_metadata_path
    common = load_package_runtime_module(
        repository / '.trellis/guru-team/scripts/bash/run-skill-command.sh', 'guru-check-task', 'common')
    projection = DeliveryProjection(repository, facts['task_ref'])
    delivery = projection.resolve(facts['delivery_key'])
    base = delivery['candidate']['base_ref']
    head = run_git(repository, 'rev-parse', 'HEAD')
    committed = run_git(repository, 'diff', '--name-only', base, head).splitlines()
    dirty = common.dirty_paths(repository)
    paths = sorted({path for path in [*committed, *dirty] if not reviewed_content_metadata_path(path)})
    candidate = projection.candidate(paths, head_ref=head, base_ref=base)
    from adapters.eval.eval_support import qualification_planning_identity
    qualification_target = {**facts['original_candidate'], 'checkout_head': head,
        'planning_identity': qualification_planning_identity(repository, [
            facts['planning_root'] + '/' + name for name in ('prd.md', 'design.md', 'implement.md')])}
    return {'current_head': head, 'fixed_base': base, 'dirty_paths': dirty,
            'reviewed_paths': paths, 'candidate': candidate,
            'reviewed_content_sha256': common.content_identity(repository),
            'architecture_candidate': {'head': head,
                'content_identity': 'sha256:' + reviewed_content_identity(repository)['sha256']},
            'diff': run_git(repository, 'diff', base), 'current_delivery': delivery,
            'qualification_target': qualification_target,
            'current_selection': projection.current(facts['delivery_key'])}


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

The pre-implementation snapshot supplied for original plan acceptance contains an interval.contains
stub raising NotImplementedError and the existing range_filter.select comprehension. Later candidate
implementation and assertions must be read from their actual files; this snapshot is historical evidence.
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

Implement R1/D1-S1/S2 and whole Task AC1..AC3. Fixed development baseline B is `{base_ref}`, selected by original DeliveryProjection.content_base from the observed business baseline HEAD. That baseline commit precedes Task/Delivery creation and this planning seed. B already contains the predicate stub, existing filter, four tests and canonical range/Architecture documents. Planning H0 was that observed HEAD; PR target main is separate. Later target observations do not redefine B.
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
    fixture = fixture.resolve()
    from adapters.eval.planning_authoring import acquire_authoring_checkout, register_authoring_resources
    acquisition = acquire_authoring_checkout(fixture, branch_name='eval/implementation')
    case_id = request['case_id']
    plan_conflict = case_id == 'native-implementation-plan-premise'
    authority_conflict = case_id == 'native-implementation-authority-conflict'
    # Reuse the actual installed creation/activation seed used by the existing
    # Phase 2 fixture. Its pre-existing approvals are fixture facts, not evidence
    # that this native invocation reviewed the accepted plan.
    with tempfile.TemporaryDirectory(prefix='implementation-seed-') as temporary:
        workdir = Path(temporary)
        write_json(workdir / 'public.json', {'profile': 'delivery_initial_check', 'mode': 'workflow', 'task_ref': '.trellis/tasks/current'})
        (workdir / 'interval.py').write_text('def contains(value, lower, upper):\n    return lower <= value < upper\n')
        phase2_authoring.stage({**request, 'workdir': temporary,
            'case_id': 'native-owner-common-expectation' if plan_conflict else 'native-owner-finding',
            'files': ['public.json', 'interval.py']}, fixture,
            fixture / '.trellis/guru-team/skills/packages/guru-check-task', source_repo,
            seed_bodies=_code_drift_seed_bodies() if case_id == 'native-implementation-code-drift' else None,
            range_authority_body=_implementation_range_authority(case_id))
    original_facts = json.loads((fixture / phase2_authoring.FACTS).read_text())
    check_input = json.loads((fixture / 'docs/phase2-evidence/check-public-input.json').read_text())
    from runtime.delivery_projection.adapter import DeliveryProjection
    from runtime.delivery_projection.gates import rework
    projection = DeliveryProjection(fixture, check_input['task_ref'])
    key = check_input['delivery_key']
    resources = register_authoring_resources(fixture, key, acquisition)
    task_ref = check_input['task_ref']
    planning = projection.planning_directory(key).relative_to(fixture).as_posix()
    reason = projection.resolve(key)['scope_ref']['authority']
    rework(projection, key, 'check', 'implementation', reason, ['check', 'full_review', 'readiness'])
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
    public = {'profile': 'delivery_initial_review', 'mode': 'workflow',
              'task_ref': task_ref, 'delivery_key': key,
              'source_selection': [{'locator': 'docs/range.md', 'section': 'Integer Range',
                                    'authority_kind': 'requirement'}]}
    if authority_conflict:
        public = {'profile': 'delivery_active_task_scope_change', 'mode': 'workflow',
            'task_ref': task_ref, 'delivery_key': key, 'source_exit': 'implementation_discovery',
            'target_locator': new_evidence, 'resume_target': 'guru-resume-implementation',
            'continuation_id': 'implementation-authority-current'}
    elif case_id == 'native-implementation-code-drift':
        public = check_input
    write_json(fixture / PUBLIC_INPUT, public)
    reads = ['.trellis/workflow.md', task_ref + '/prd.md', *[planning + '/' + name for name in ('prd.md', 'design.md', 'implement.md')],
             'docs/range.md', new_evidence, 'interval.py', 'range_filter.py', 'test_interval.py',
             'docs/operator-notes.md', 'docs/phase2-evidence/validation.json',
             'docs/architecture/README.md', 'docs/architecture/00-foundation/design-constitution.md',
             'docs/architecture/06-governance/change-contract.md', phase2_authoring.ARCHITECTURE_INPUT]
    if authority_conflict:
        reads.extend([
            '.trellis/guru-team/skills/packages/guru-clarify-requirements/schemas/public-delivery-active-task-scope-change-input.schema.json',
            '.trellis/guru-team/skills/packages/guru-clarify-requirements/schemas/semantic-scope-continuation-2.0.schema.json',
        ])
    owner_reads = []
    for skill in OWNERS:
        owner = fixture / '.trellis/guru-team/skills/packages' / skill
        owner_reads.extend(str(path.relative_to(fixture)) for path in (
            owner / 'SKILL.md', owner / 'interface.json', owner / 'commands.json') if path.is_file())
    rdt = fixture / '.trellis/guru-team/skills/packages' / RDT
    rdt_interface = json.loads((rdt / 'interface.json').read_text())
    rdt_reads = ('references/contract.md','references/current-knowledge.md',
        'schemas/public-input-impact-2.0.schema.json','schemas/semantic-result.schema.json',
        *[output['schema']['path'] for output in rdt_interface['public_contracts']['outputs']])
    owner_reads.extend((rdt / relative).relative_to(fixture).as_posix() for relative in rdt_reads)
    from adapters.eval.owner_runtime import load_package_runtime_module
    approval = load_package_runtime_module(
        fixture / '.trellis/guru-team/scripts/bash/run-skill-command.sh',
        'guru-approve-task-plan', 'common')
    approval_checkpoint = approval.checkpoint(
        fixture, fixture / task_ref, 'planning-approval.json', key).relative_to(fixture).as_posix()
    write_json(fixture / FACTS, {'schema_version': '1.0',
        'required_reads': reads + owner_reads, 'public_input_locator': PUBLIC_INPUT,
        'task_ref': task_ref, 'delivery_key': key, 'planning_root': planning,
        'seed_boundary': 'Existing approved plan is a starting fixture fact; it is not a native review result.',
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
        **({'planning_candidate_syntax':
            'For original Planning candidate_assessment without a design_locator, freshness_identity must be "sha256:" plus the SHA256 hex digest of json.dumps(candidate, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"). Compute this from your own actual candidate object; the existing run command can perform the calculation. The worktree and planning-file identities returned by inspect describe different objects and are not this call-local candidate digest.'
        } if case_id == 'native-implementation-plan-premise' else {}),
        **({'execution_surface': [
            *EXECUTION_SURFACE,
            *(['Original recorder/checker stdout is an intermediate receipt. A Check recorder receipt includes artifact_path and dry_run; those receipt fields are not Phase 2 semantic-result properties. Use the emitted artifact_path with the original public wrapper owner-result argument, according to its current Interface, instead of embedding the complete receipt as owner_result.',
               'For the supported JSON file form of original record-phase2-check --input, author your own recorder form bytes and use the existing implementation-authoring run command to write them to .trellis/.runtime/guru-team/evals/phase2-owner-input.json, then pass that relative locator. After the recorder consumes it, remove that transient input with the same run capability. This uses the existing private eval input path and execution capability; it does not expand the permitted final inventory.']
              if case_id == 'native-implementation-code-drift' else []),
        ]} if case_id in ('native-implementation-code-drift', 'native-implementation-authority-conflict') else {}),
    })


def context(repository: Path, package: Path, helper_command: str, reads: list[str], input_locator: Path, *, facts_relative: str = FACTS) -> str:
    return '\n'.join([
        ('Continue the same fixture from the actual preceding owner output and current public state. Read the installed workflow mapping and original owner contracts to select and execute the applicable continuation yourself. The preceding output is not a next-owner input; author that input from the actual producer result and current facts.'
         if facts_relative == PLANNING_CONTINUATION_FACTS else
         'Continue the current implementation under the installed workflow and original owner contracts. The starting accepted plan and newly available source evidence are supplied as files.'),
        f'Repository: {repository}', f'Fact sheet: {repository / facts_relative}',
        *[f'{helper_command} read --kind owner_file --path {repository / path}' for path in reads],
        f'{helper_command} read --kind owner_file --path {input_locator}',
        'Read the supplied current workflow, source, planning, implementation, tests and caller files. Load the original owner contract and exact input/output schemas for each command you select.',
        'Complete the fact-sheet read and every helper read listed in its required_reads before the first helper command, including help, contract and inspect.',
        'Run every helper read and command sequentially. Wait for the current helper process and its complete response before starting any other helper, including while an independent Architecture review is running. Do not leave a helper running while you inspect more files or start another command.',
        'Use the private helper command transport repeatedly: helper command --skill-id <original skill-id> --command <original command-id or invoke> --stdin -- <original argv>. Its stdin is the original command stdin. For installed Delivery APIs use skill-id delivery-api. The helper inserts the selected command once; arguments after -- contain only that command\'s arguments, not the command name again. Read actual API capabilities with helper command --skill-id delivery-api --command contract -- --json. Read top-level syntax with helper command --skill-id delivery-api --command=--help, and selected syntax with helper command --skill-id delivery-api --command <subcommand> -- --help before choosing its exact arguments. These calls execute the original delivery.py in the owner checkout. To transport your own bounded file bytes, use skill-id implementation-authoring, command write, and stdin {file_updates:{relative_path:complete_text}}. No host-generated intermediate DTO or route is supplied.',
        'Only the final original semantic wrapper call uses eval-only stdin {final:true,invocation:<your original stdin envelope>}; the helper removes those transport fields before the original wrapper. Use command invoke with the exact original argv of the selected wrapper. For a wrapper supporting --invocation -, invocation supplies its actual stdin object. Author uses --input <JSON> --owner-result <JSON> instead; author those original JSON arguments yourself and leave invocation as an empty object for its unused stdin. Earlier wrapper outputs remain their own original producer results.',
        'For original Check filename invocation, use --input <public-input locator> --owner-result <semantic-result locator>. In its --invocation envelope, owner_result must be the original checked semantic JSON object, not a path string or recorder receipt.',
        'For any required independent Architecture assessment, use command --skill-id guru-maintain-architecture-baseline --command independent-review --stdin with {public_input:<your actual original input>,reads:[<ordered repository-relative authority, candidate and consumer locators>]}. This private transport launches the existing fresh generic Architecture worker with the original reviewer prelude and returns its actual original wrapper stdout. Supply locators and original input only; never supply its owner_result, finding or exit. Direct Architecture self-assessment from this implementation context is unavailable.',
        *EXECUTION_SURFACE,
        'When that original Architecture result itself ends the current segment under its contract, the same final:true transport envelope can end independent-review and return the actual Architecture stdout. No additional caller-authored semantic result is needed merely to expose its original exit.',
        'To observe the actual current full candidate after writes, use command --skill-id implementation-authoring --command inspect with empty stdin. It returns actual head/base, complete changed paths, original content identities, full diff and public Delivery state. To run an actual validation, use command --skill-id implementation-authoring --command run --stdin with {argv:[<explicit executable and arguments>]}; it runs in the fixture and returns the real process output. These commands make no semantic judgment or route selection.',
        'Recorder/checker stdout is an intermediate receipt, not a public owner exit. Preserve and project actual results under the original owner contract; keep them in memory and do not reconstruct semantic results from a prior pass. All paths and original command arguments refer to the installed fixture root, not the evidence projection. Use relative paths for original --input/--owner-result file locators returned by that owner.',
        ('This invocation consumes actual prior Activation output and current public Delivery facts for the same fixture. Continue under the installed workflow and the original owners\' current responsibilities. Determine from the current source, plan, applicable reviews and candidate whether affected implementation can resume. If current facts require re-entry, follow the original workflow and owner contracts.'
         if facts_relative == RESUME_FACTS else
         'If this invocation reaches Planning Approval approved, make that original invoke the final call and return its actual stdout. The ordinary workflow plan presentation/acceptance and Activation happen outside this native segment. Do not activate the Delivery, claim acceptance, or restore affected implementation in this segment. A later independently declared test invocation can consume actual Activation/public-current facts. Other original stop/re-entry outcomes remain available under their actual contracts.'),
        'Return only the final original semantic owner wrapper stdout. Preserve every failed original command. An original Delivery CLI argument-parse error leaves this transport open so you can read its help and correct your own arguments. The host does not change arguments or select a continuation. Other Delivery execution failures and every nonzero original owner wrapper end this invocation; never synthesize a successful result.',
    ])


class ImplementationCommands:
    """Private command transport; the native owner selects every continuation."""

    def __init__(self, repository: Path, environment: dict, receipts_path: Path, *, facts_relative: str = FACTS):
        self.repository = repository
        self.environment = environment
        self.receipts_path = receipts_path
        self.facts_relative = facts_relative
        self.receipts = []
        self.terminal = False
        self.independent_reviewer = None

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
        if stdin:
            value = json.loads(stdin)
            if isinstance(value, dict) and 'final' in value and 'invocation' in value:
                final = value['final'] is True
                stdin = json.dumps(value['invocation'], ensure_ascii=False)
        if skill == 'guru-maintain-architecture-baseline':
            if command != 'independent-review' or self.independent_reviewer is None:
                raise ValueError('Architecture assessment requires its actual fresh independent worker')
            result = self.independent_reviewer(json.loads(stdin))
            self.record_response(payload, result)
            if result['returncode'] or final:
                self.terminal = True
            return result
        if skill == 'implementation-authoring' and command == 'inspect':
            facts = json.loads((self.repository / self.facts_relative).read_text())
            result = {'returncode': 0, 'stdout': json.dumps(observe_candidate(self.repository, facts)) + '\n', 'stderr': ''}
            self.record_response(payload, result)
            return result
        if skill == 'implementation-authoring' and command == 'run':
            argv = json.loads(stdin)['argv']
            process = subprocess.run(argv, cwd=self.repository, env=self.environment,
                text=True, capture_output=True, check=False)
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
            if skill not in OWNERS:
                raise ValueError('implementation command has no supplied existing owner')
            owner = self.repository / '.trellis/guru-team/skills/packages' / skill
            interface = json.loads((owner / 'interface.json').read_text())
            command_id = interface['public_contracts']['invocation']['command_id'] if command == 'invoke' else command
            # Some Interfaces name the shared dispatcher. The selected public
            # wrapper still declares one concrete command in its launcher.
            if command_id == 'run-skill-command':
                command_id = 'invoke-' + skill
            commands = json.loads((owner / 'commands.json').read_text())['commands']
            if not any(row['id'] == command_id for row in commands):
                raise ValueError('implementation command is not declared by its original owner')
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
        delivery_parse_error = (skill == 'delivery-api' and process.returncode == 2
            and not process.stdout and process.stderr.startswith('usage: delivery.py ')
            and any(prefix in process.stderr for prefix in (
                '\ndelivery.py: error:', f'\ndelivery.py {command}: error:')))
        if process.returncode and not delivery_parse_error:
            self.terminal = True
        if final and process.returncode == 0:
            if skill == 'delivery-api' or command != 'invoke':
                raise ValueError('only an original semantic public wrapper can terminate implementation evidence')
            self.terminal = True
        return result


def owner_schema(package: Path) -> str:
    return {
        'guru-author-task-plan': 'schemas/semantic-result-2.0.schema.json',
        'guru-check-task': 'schemas/phase2-check.schema.json',
        'guru-clarify-requirements': 'schemas/semantic-scope-continuation-2.0.schema.json',
    }[json.loads((package / 'interface.json').read_text())['id']]


def public_reads(package: Path) -> tuple[str, ...]:
    identity = json.loads((package / 'interface.json').read_text())['id']
    reference = 'references/authoring.md' if identity == 'guru-author-task-plan' else 'references/contract.md'
    return (*PUBLIC_READS, reference, owner_schema(package))


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
    final = json.loads(last['request']['stdin'])
    if (last['request']['command'] not in {'invoke', 'independent-review'} or final.get('final') is not True
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
